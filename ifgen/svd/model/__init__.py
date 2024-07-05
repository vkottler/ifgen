"""
A module implementing a data model for ARM CMSIS-SVD 'device' data.
"""

# built-in
from dataclasses import dataclass
from typing import Any, Optional
from xml.etree import ElementTree

# internal
from ifgen.svd.model.cpu import Cpu
from ifgen.svd.model.device import Device
from ifgen.svd.model.peripheral import Peripheral


@dataclass
class SvdModel:
    """A model for SVD data."""

    peripherals: dict[str, Peripheral]
    device: Optional[Device] = None
    cpu: Optional[Cpu] = None

    @property
    def device_name(self) -> str:
        """Get the SVD device name."""
        assert self.device is not None
        return self.device.raw_data["name"]

    def namespace(self) -> list[str]:
        """Get a namespace for this SVD device."""
        return [x.upper() for x in self.device_name.split("_")]

    def metadata(self) -> dict[str, Any]:
        """Get device and CPU metadata."""

        result: dict[str, Any] = {}

        if self.device is not None:
            result["device"] = self.device.raw_data
        if self.cpu is not None:
            result["cpu"] = self.cpu.raw_data

        for name, peripheral in self.peripherals.items():
            data = {
                "interrupts": [x.raw_data for x in peripheral.interrupts],
                "address_blocks": [
                    x.raw_data for x in peripheral.address_blocks
                ],
            }

            # Add alternate group metadata.
            groups = peripheral.register_groups()
            if groups:
                data["register_groups"] = {  # type: ignore
                    key: [x.name for x in value]
                    for key, value in groups.items()
                }

            result[name] = data

        return result

    def assign_device(self, device: Device) -> None:
        """Assign a device instance."""
        assert self.device is None, self.device
        self.device = device

    def assign_cpu(self, cpu: Cpu) -> None:
        """Assign a cpu instance."""
        assert self.cpu is None, self.cpu
        self.cpu = cpu

    def register_peripheral(
        self, elem: ElementTree.Element, peripheral: Peripheral
    ) -> None:
        """Register a peripheral."""

        name = peripheral.raw(elem)["name"]
        assert name not in self.peripherals, f"Duplicate peripheral '{name}'!"
        self.peripherals[name] = peripheral
