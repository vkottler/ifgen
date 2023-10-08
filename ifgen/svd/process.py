"""
A module implementing interfaces for processing registers and clusters.
"""

# built-in
from xml.etree import ElementTree

# internal
from ifgen.svd.model.field import get_fields
from ifgen.svd.model.peripheral import (
    Cluster,
    Peripheral,
    Register,
    RegisterData,
)

ClusterMap = dict[str, "Cluster"]
RegisterMap = dict[str, Register]


def handle_registers(
    registers: ElementTree.Element,
    peripheral: Peripheral,
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
                cluster(
                    item, cluster_map, peripheral, register_map=register_map
                )
            )
        elif item.tag == "register":
            result.append(register(item, register_map, peripheral))

    return result


def cluster(
    element: ElementTree.Element,
    cluster_map: ClusterMap,
    peripheral: Peripheral,
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
            element,
            peripheral,
            cluster_map=cluster_map,
            register_map=register_map,
        ),
        peripheral,
    )
    cluster_map[inst.name] = inst
    return inst


def register(
    element: ElementTree.Element,
    register_map: RegisterMap,
    peripheral: Peripheral,
) -> Register:
    """Create a Register instance from an SVD element."""

    derived_register = None
    derived = element.attrib.get("derivedFrom")
    if derived is not None:
        derived_register = register_map[derived]  # pragma: nocover

    # Handle writeConstraint at some point?

    # Load fields.
    fields = None
    fields_elem = element.find("fields")
    if fields_elem is not None:
        fields = get_fields(fields_elem)

    inst = Register.create(element, derived_register, fields, peripheral)
    register_map[inst.name] = inst

    # Keep track of alternates.
    if inst.is_alternate():
        alt = inst.alternate()
        assert alt is not None
        register_map[alt].alternates.append(inst)

    return inst
