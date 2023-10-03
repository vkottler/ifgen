"""
A module implementing a 'peripherals' SVD-element processor.
"""

# built-in
from xml.etree import ElementTree

# third-party
from vcorelib.logging import LoggerType

# internal
from ifgen.svd.model.peripheral import Peripheral
from ifgen.svd.task import SvdProcessingTask


def process_peripheral(
    elem: ElementTree.Element, task: SvdProcessingTask, logger: LoggerType
) -> None:
    """Process a SVD peripheral element."""

    derived_periph = None
    derived = elem.attrib.get("derivedFrom")
    if derived is not None:
        derived_periph = task.model.peripherals[derived]

    peripheral = Peripheral(derived_periph)
    peripheral.log(elem, logger)

    if derived_periph is not None:
        logger.info(
            "Peripheral '%s' derived from '%s'.",
            peripheral.name,
            derived_periph.name,
        )

    # addressBlock

    # interrupt

    # registers

    task.model.register_peripheral(elem, peripheral)


def process_peripherals(
    elem: ElementTree.Element, task: SvdProcessingTask, logger: LoggerType
) -> None:
    """Process a SVD peripherals element."""

    elem_stack = []

    del logger
    for peripheral in elem.iterfind("peripheral"):
        # Handle derived peripherals last.
        derived = peripheral.attrib.get("derivedFrom")
        if derived is not None:
            elem_stack.append(peripheral)
        else:
            elem_stack.insert(0, peripheral)

    while elem_stack:
        task.process(elem_stack.pop(0))
