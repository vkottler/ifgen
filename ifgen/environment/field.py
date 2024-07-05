"""
A module implementing interfaces for processing individual struct fields.
"""

# built-in
from typing import Any, Iterator

# third-party
from runtimepy.codec.system import TypeSystem

# internal
from ifgen.environment.padding import PaddingManager, StructField, type_string


def process_field(
    struct_name: str,
    padding: PaddingManager,
    types: TypeSystem,
    field: dict[str, Any],
    namespace: list[str],
) -> Iterator[StructField]:
    """Process a single struct field."""

    field_name = field["name"]

    # Validate expected offset.
    if "expected_offset" in field:
        size = types.size(struct_name, *namespace)
        expected: int = field["expected_offset"]

        difference = expected - size

        assert difference >= 0, (
            f"{difference} ({struct_name}.{field_name}) current={size} "
            f"!= expected={expected}"
        )

        # Add padding automatically.
        if difference > 0:
            for padding_field in padding.add_padding(difference):
                # Padding should never generate more padding.
                assert not list(
                    process_field(
                        struct_name, padding, types, padding_field, namespace
                    )
                )

                # The caller is responsible for updating the container for
                # fields.
                yield padding_field

    types.add(
        struct_name,
        field_name,
        type_string(field["type"]),
        array_length=field.get("array_length"),
        exact=False,
    )
