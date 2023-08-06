import itertools
import threading
from typing import Callable, List, Union, Optional

import networkx as nx

import _feyn
from feyn import Graph
import feyn.losses

FittingShowType = Union[str, Callable[[Graph, float], None]]

class QGraph:
    """
    A QGraph is extracted from the QLattice with the `QLattice.get_qgraph()` method. It contains a very large number of possible models linking a set of input registers to an output registers.

    After it has been extracted, the QGraph is fitted with a data set to solve a specific task.

    The constructor is for internal use. QGraphs should always be generated with the `QLattice.get_graph` method.

    Arguments:
        graph_dict -- A dictionary containing the QGraph descriptor.
    """

    def __init__(self, graph_dict: dict):
        """Construct a new `QGraph` object."""
        self.G = nx.readwrite.json_graph.node_link_graph(graph_dict)

        self.out_reg_dict = graph_dict["out_reg"]

        self._graphs = self._extract_graphs()

    def head(self, n:int=5) -> None:
        """
        Render a selection of Graphs from the QGraph.

        Arguments:
            n -- Number of graphs to display.
        """
        import IPython
        for i in range(n):
            IPython.display.display(self._graphs[i])


    def _update_display(self, current_ix, best_ix, show):
        status = "Examined %i of %i. Best loss so far: %.6f" % (current_ix+1, len(self._graphs), self._graphs[best_ix].loss_epoch)

        if show == "graph":
            import IPython
            svgdata = feyn._current_renderer.rendergraph(self._graphs[best_ix], status)
            IPython.display.clear_output(wait=True)
            IPython.display.display(IPython.display.SVG(svgdata))

        elif show == "text":
            print(status)
        elif callable(show):
            show(self._graphs[best_ix], self._graphs[best_ix].loss_epoch)
        elif show is None:
            pass
        else:
            raise Exception("show must be either None, 'graph' or 'text', or a callback function")



    def fit(self, data, epochs:int=10, loss_function=_feyn.DEFAULT_LOSS, show:Optional[FittingShowType]="graph", threads:int=1) -> None:
        """
        Fit `QGraph` with given data set.

        Arguments:
            data -- Training data including both input and expected values. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            epochs -- Number of epochs to run.
            loss_function -- Name of the loss function or the function itself. This is the loss function to use for fitting. Can either be a string or one of the functions provided in `feyn.losses`.
            show -- Controls status display. If specified, it should be either "graph", "text", or a user-defined callback function which recieves the best graph found so far, along with it's loss.
            threads -- Number of concurrent threads to use for fitting. Choose this number to match the number of CPU cores on your machine.
        """
        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        loss_function = feyn.losses._get_loss_function(loss_function)
        if not hasattr(loss_function, "c_derivative"):
            raise ValueError("Loss function cannot be used for fitting, since it doesn't have a corresponding c derivative")

        _best_ix = None
        _current_ix = 0
        _counter = itertools.count()
        _terminate = False
        _exception: BaseException = None

        def fitting_thread():
            nonlocal _terminate, _best_ix, _current_ix, _counter, _exception, epochs, self
            try:
                while not _terminate:
                    ix = next(_counter)
                    if ix >= len(self._graphs):
                        return
                    _current_ix = ix
                    g = self._graphs[ix]
                    g._fit(data, epochs=epochs, loss_function=loss_function)
                    if _best_ix == None or g.loss_epoch <= self._graphs[_best_ix].loss_epoch:
                        _best_ix = ix
            except BaseException as e:
                _exception = e

        threadlist = [threading.Thread(target=fitting_thread) for num in range(threads)]

        try:
            [t.start() for t in threadlist]
            while True in [t.is_alive() for t in threadlist]:
                [t.join(1/threads) for t in threadlist]
                if _exception:
                    raise _exception
                self._update_display(_current_ix, _best_ix, show)
        finally:
            _terminate=True
            [t.join() for t in threadlist]
        if _exception:
            raise _exception

        self._graphs.sort(key=lambda g: g.loss_epoch, reverse=False)


    def select(self, data, loss_function=_feyn.DEFAULT_LOSS, max_depth=-1, max_edges=-1, n=5) -> List[Graph]:
        """
        Select a filtered and sorted list of graphs. The selection is based on the loss of each graph against the provided data set or other custom criterias.

        # Fit and select a graph from a qgraph
        >>> graph.fit(training_data, loss_function=feyn.losses.mean_squared_error)
        >>> g = graph.select(some_other_data, loss_function=feyn.losses.mean_absolute_error)

        Arguments:
            data -- The data set to select by. Can be either a dict mapping register names to value arrays, or a pandas.DataFrame.
            loss_function -- The loss function to use when selecting graphs. Can either be a string or one of the functions provided in `feyn.losses`.
            max_depth -- The maximum depth of the graphs selected. -1 means unlimited.
            max_edges -- The maximum number of edges in the graphs selected. -1 means unlimited.
            n -- Max number of graphs to return.

        Returns:
            List[Graph] -- The list of up to `n` selected graphs.
        """
        # Magic support for pandas DataFrame
        if type(data).__name__ == "DataFrame":
            data = {col: data[col].values for col in data.columns}

        graph_collection = self._graphs.copy()

        if max_depth != -1:
            graph_collection = list(filter(lambda g: g[-1].depth<=max_depth, graph_collection))

        if max_edges != -1:
            graph_collection = list(filter(lambda g: g.edge_count<=max_edges, graph_collection))

        loss_func = feyn.losses._get_loss_function(loss_function)

        data_losses = {}
        for graph in graph_collection:
            out_reg = graph[-1]
            l = loss_func(data[out_reg.name], graph.predict(data))
            data_losses[graph] = l

        graph_collection.sort(key=lambda g : data_losses[g], reverse=False)

        return graph_collection[0:n]


    def _extract_graphs(self) -> List[Graph]:
        graphs = set()

        for nodeid, data in self.G.nodes(data=True):
            if data["type"] != "reg":
                graphs.add(self._prune(nodeid))

        return sorted(graphs, key=lambda n: n.strength, reverse=True)

    def _prune(self, nodeid: int) -> Graph:
        needed = nx.algorithms.dag.ancestors(self.G, nodeid)
        needed.add(nodeid)
        subgraph = self.G.subgraph(needed)

        # The following algorithm builds a 1D array of nodes
        # that preserverves execution order
        nodelist = []
        current = [nodeid]
        while len(current) > 0:
            node = current.pop(0)
            if node in nodelist:
                nodelist.remove(node)
            nodelist.insert(0, node)
            for pred in subgraph.predecessors(node):
                current.append(pred)

        # Build a graph with the interactions
        sz = len(nodelist)+1
        graph = Graph(sz)

        for i, nodeid in enumerate(nodelist):
            data = subgraph.nodes[nodeid]

            interaction = Graph._get_interaction(data)
            graph[i] = interaction

            if data["type"]=="reg":
                interaction._set_source(0, -1)
                continue

            interaction._linkdata = [None, None]

            for pred, _, data in subgraph.in_edges(nodeid, data=True):
                source_idx = nodelist.index(pred)
                ordinal = data["ord"]
                interaction._set_source(ordinal, source_idx)
                interaction._linkdata[ordinal] = data

        out_reg = Graph._get_interaction(self.out_reg_dict)
        out_reg._linkdata = [{"ord": 0}]

        out_reg._set_source(0, sz-2)

        graph[sz-1] = out_reg

        graph.strength = self.G.nodes[nodeid]["output_strength"]

        return graph


    def __repr__(self):
        regcnt = 0
        double = 0
        single = 0
        for _, data in self.G.nodes.data():
            if data["type"] == "reg":
                regcnt += 1

            else:
                legs = data["legs"]
                if legs == 1:
                    single += 1
                else:
                    double += 1

        out_name = self.out_reg_dict["name"]
        return "QGraph for '%s' <size: %i (%i registers, %i singles, %i doubles)>" % (out_name, regcnt+double+single, regcnt, single, double)
