import os
from datetime import datetime
from typing import List, Tuple, Union, cast

import requests

import _feyn
import feyn
from feyn import Graph, QGraph, SnapshotCollection

from ._register import Register, RegisterCollection

class QLattice:
    """
    A QLattice (short for Quantum Lattice) is a device which can be used to generate and explore a vast number of models linking a set of input observations to an output prediction.

    The QLattice stores and updates probabilistic information about the mathematical relationships (models) between observable quantities.

    The actual QLattice runs on a dedicated computing cluster which is operated by Abzu. The `feyn.QLattice` class provides a client interface to communcate with, extract models from, and update the QLattice.

    The workflow is typically:
    1) extract a QGraph from the QLattice using `QLattice.get_qgraph`.
    2) fit the QGraph to a local dataset using `QGraph.fit`.
    3) select one or more models from the QGraph using `QGraph.select`.
    4) potentially update the QLattice with new knowledge using `QLattice.update`.

    Arguments:
        url -- URL of your QLattice.
        api_token -- Authentication token for the communicating with this QLattice.
    """

    _QLATTICE_BASE_URI = os.environ.get('QLATTICE_BASE_URI') or 'http://localhost:5000'

    def __init__(self, url: str=None, api_token: str=None):
        """Construct a new 'QLattice' object."""
        if url is None:
            url = self._QLATTICE_BASE_URI

        url += "/api/v1/qlattice"

        self.url = url

        if api_token == None:
            api_token = os.environ.get('FEYN_TOKEN', "none")

        self.headers = {
            'Authorization': f'Bearer {api_token}',
            'User-Agent': f"feyn/{feyn.__version__}"
        }

        self._load_qlattice()

        self._snapshots = SnapshotCollection(self)
        self._registers = RegisterCollection(self)

    def get_register(self, name: str, register_type: str = "fixed") -> Register:
        """
        This method is deprecated and will be removed in the future. It does the same as:
        >>> qlattice.registers.get(name, regtype)
        """
        return self.registers.get(name, register_type)

    def get_qgraph(self, registers: List[Union[str,Register]], output: Union[str,Register], max_depth: int = 5) -> QGraph:
        """
        Extract QGraph from inputs registers to an output register.

        The standard workflow for QLattices is to extract a QGraph using this function. You specify a list of input registers corresponding to the input values you want to use for predictions, and a single output register corresponding to the output variable you want to predict.

        Once the QGraph has been extracted from the QLattice, you'll typically use the `QGraph.fit()` function to fit the QGraph to an actual dataset, and then `QGraph.select()` to select the final model.

        Arguments:
            registers -- List of registers or names to use in the QGraph.
            output -- The output register or name.
            max_depth -- The maximum depth of the graphs.

        Raises:
            ValueError -- Raised if one of the specified registers does not exist in the QLattice. You should always ensure that the registers have been added using QLattice.registers.get().

        Returns:
            QGraph -- The QGraph instance from the inputs to the output.
        """

        # Convert possible registers in to plain strings
        inputs = [str(reg) for reg in registers]
        output = str(output)

        if output in inputs:
            inputs.remove(output)

        req = requests.post("%s/simulation" % self.url,
                            headers=self.headers,
                            json={
                                'inputs': inputs,
                                'output': output,
                                'max_depth': max_depth
                            })

        if req.status_code == 422:
            raise ValueError(req.text)

        req.raise_for_status()

        graph = req.json()

        qgraph = QGraph(graph)

        return qgraph

    def update(self, graph: Graph) -> None:
        """
        Update QLattice with learnings from a `Graph`.

        When updated, The QLattice learns to produce better and better QGraphs. This is how a QLattice evolves and narrows in on producing QGraphs with better and better models.

        Without updating, the QLattice will not learn about good models and the QGraphs produced from the QLattice will not contain better models.

        # Select the best Graph from the QGraph and update the QLattice with it's learnings
        >>> graph = qgraph.select(data)[0]
        >>> ql.update(graph)

        Arguments:
            graph -- Graph with learnings worth storing.
        """
        req = requests.post("%s/update" % self.url,
                            headers=self.headers,
                            json=graph._to_dict()
                            )

        req.raise_for_status()

    @property
    def snapshots(self):
        """
        Collection of snapshots for this QLattice

        Use this collection to capture, list and restore the complete state of a QLattice.
        """
        return self._snapshots

    @property
    def registers(self):
        """
        The RegisterCollection of the QLattice

        The RegisterCollection is used to find, create and remove registers from the QLattice.
        """
        return self._registers

    def reset(self) -> None:
        """
        Clear all learnings in this QLattice.

        This is a potentially dangerous action. Think twice before calling this method.
        """
        req = requests.post(f"{self.url}/reset", headers=self.headers)
        req.raise_for_status()

        self._load_qlattice()

    def __repr__(self):
        return "<Abzu QLattice[%i,%i] '%s'>" % (self.width, self.height, self.url)

    def _load_qlattice(self):
        req = requests.get(self.url, headers=self.headers)

        # The purpose of this special handling is to create a channel for messaging the user about issues that we have somehow 
        # failed to consider beforehand.
        if req.status_code == 400:
            raise ConnectionError(req.text)

        req.raise_for_status()

        qlattice = req.json()

        self.width = qlattice['width']
        self.height = qlattice['height']
