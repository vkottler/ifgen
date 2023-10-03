"""
A module implementing a data model for ARM CMSIS-SVD 'device' data.
"""

# built-in
from dataclasses import dataclass
from typing import Optional

# internal
from ifgen.svd.model.cpu import Cpu
from ifgen.svd.model.device import Device


@dataclass
class SvdModel:
    """A model for SVD data."""

    device: Optional[Device] = None
    cpu: Optional[Cpu] = None

    def assign_device(self, device: Device) -> None:
        """Assign a device instance."""
        assert self.device is None, self.device
        self.device = device

    def assign_cpu(self, cpu: Cpu) -> None:
        """Assign a cpu instance."""
        assert self.cpu is None, self.cpu
        self.cpu = cpu
