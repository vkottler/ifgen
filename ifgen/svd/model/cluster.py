"""
A module implementing a data model for ARM CMSIS-SVD 'cluster' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, Optional
from xml.etree import ElementTree

# internal
from ifgen.svd.model.derived import DerivedMixin, derived_from_stack
from ifgen.svd.model.device import ARRAY_PROPERTIES, REGISTER_PROPERTIES
from ifgen.svd.string import StringKeyVal


@dataclass
class Cluster(DerivedMixin):
    """A container for cluster information."""

    derived_from: Optional["Cluster"]

    @classmethod
    def string_keys(cls) -> Iterable[StringKeyVal]:
        """Get string keys for this instance type."""

        # Not currently handling nested registers or clusters.

        return (
            ARRAY_PROPERTIES
            + [
                StringKeyVal("name", True),
                StringKeyVal("description", False),
                StringKeyVal("alternateCluster", False),
                StringKeyVal("headerStructName", False),
                StringKeyVal("addressOffset", True),
            ]
            + REGISTER_PROPERTIES
        )


ClusterMap = dict[str, Cluster]


def get_clusters(registers: ElementTree.Element) -> ClusterMap:
    """Get register clusters."""

    result: ClusterMap = {}
    for cluster in derived_from_stack(registers.iterfind("cluster")):
        derived_cluster = None
        derived = cluster.attrib.get("derivedFrom")
        if derived is not None:
            derived_cluster = result[derived]  # pragma: nocover

        inst = Cluster.create(cluster, derived_cluster)
        result[inst.name] = inst

    return result
