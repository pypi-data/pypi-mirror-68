"""Feyn is the main Python module to build and execute models that utilizes a QLattice.

A QLattice (short for Quantum Lattice) is a device which can be used to generate and explore a vast number of models linking a set of input observations to an output prediction. The actual QLattice runs on a dedicated computing cluster which is operated by Abzu. The `feyn.QLattice` class provides a client interface to communcate with, extract models from, and update the QLattice.

The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

The workflow is typically:

# Connect to the QLattice
>>> ql = feyn.QLattice("your-qlattice-url")

# Allocate some registers on the QLattice to serve as input and output
>>> regs = [ql.registers.get("x1"), ql.registers.get("x2"),
>>>         ql.registers.get("y")]

# Extract a QGraph
>>> qgraph = gl.get_qgraph(regs, output="y")

# Fit the QGraph to a local dataset with values for the registers (x1, x2 and y)
>>> qgraph.fit(data)

# Select the best Graph from the QGraph
>>> graph = qgraph.select(data)[0]

# Possibly update the QLattice with the graph to make the QLattice better at this kind of model in the future
>>> ql.update(graph)

# Or use the graph to make predictions
>>> predicted_y = graph.predict(new_data)
"""
import pkg_resources  # part of setuptools
from _feyn import Interaction
from ._svgrenderer import SVGRenderer
from ._graph import Graph
from ._qgraph import QGraph
from ._snapshots import SnapshotCollection, Snapshot
from ._qlattice import QLattice
from ._register import Register
from . import losses

_current_renderer = SVGRenderer

__all__ = ['QLattice', 'QGraph', 'Graph', 'Interaction', 'SnapshotCollection', 'Snapshot']

__version__ = pkg_resources.require("feyn")[0].version
