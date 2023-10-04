"""
A module implementing a data model for ARM CMSIS-SVD 'cluster' data.
"""

# built-in
from dataclasses import dataclass
from typing import Iterable, Optional, Union
from xml.etree import ElementTree

# internal
from ifgen.svd.model.derived import DerivedMixin
from ifgen.svd.model.device import ARRAY_PROPERTIES, REGISTER_PROPERTIES
from ifgen.svd.model.register import Register, RegisterMap, register
from ifgen.svd.string import StringKeyVal

ClusterMap = dict[str, "Cluster"]
RegisterData = list[Union[Register, "Cluster"]]


@dataclass
class Cluster(DerivedMixin):
    """A container for cluster information."""

    derived_from: Optional["Cluster"]
    children: RegisterData

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


def handle_registers(
    registers: ElementTree.Element,
    cluster_map: ClusterMap = None,
    register_map: RegisterMap = None,
) -> RegisterData:
    """Handle the 'registers' element."""

    result: RegisterData = []

    if cluster_map is None:
        cluster_map = {}
    if register_map is None:
        register_map = {}

    for item in registers:
        if item.tag == "cluster":
            result.append(
                cluster(item, cluster_map, register_map=register_map)
            )
        elif item.tag == "register":
            result.append(register(item, register_map))

    return result


def cluster(
    element: ElementTree.Element,
    cluster_map: ClusterMap,
    register_map: RegisterMap = None,
) -> Cluster:
    """Create a Cluster instance from an SVD element."""

    derived_cluster = None
    derived = element.attrib.get("derivedFrom")
    if derived is not None:
        derived_cluster = cluster_map[derived]  # pragma: nocover

    inst = Cluster.create(
        element,
        derived_cluster,
        handle_registers(
            element, cluster_map=cluster_map, register_map=register_map
        ),
    )
    cluster_map[inst.name] = inst
    return inst
