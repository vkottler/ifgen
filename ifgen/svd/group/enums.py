"""
A module for handling SVD bit-field enumerations.
"""

# built-in
from os.path import commonprefix
from typing import Any

# internal
from ifgen.svd.model.enum import EnumeratedValues

EnumValues = dict[str, Any]
ENUM_DEFAULTS: dict[str, Any] = {
    "unit_test": False,
    "json": False,
    "use_map": False,
    "identifier": False,
}

BY_HASH: dict[str, dict[int, str]] = {}
PRUNE_ENUMS = False


def get_enum_name(name: str, peripheral: str, raw_mapping: EnumValues) -> str:
    """Get the name of an enumeration."""

    if not PRUNE_ENUMS:
        return name

    hashed = hash(
        ",".join(
            name + f"={val['value']}" for name, val in raw_mapping.items()
        )
    )

    BY_HASH.setdefault(peripheral, {})

    for_periph = BY_HASH[peripheral]
    for_periph.setdefault(hashed, name)

    return for_periph[hashed]


IGNORE_WORDS = {
    "the",
    "as",
    "a",
    "is",
    "will",
    "but",
    "are",
    "yet",
    "that",
    "to",
    "and",
    "in",
    "of",
    "on",
    "for",
    "from",
    "its",
    "it",
}


def is_name_part(value: str) -> bool:
    """Determine if a word should be part of an enumeration value name."""
    return bool(value) and value not in IGNORE_WORDS


def as_alnum(word: str) -> str:
    """Get a word's alpha-numeric contents only."""

    result = ""
    for char in word:
        if char.isalnum() or char == "_":
            result += char

    return result


def handle_enum_name(name: str, description: str = None) -> str:
    """Attempt to generate more useful enumeration names."""

    if name.startswith("value") and description:
        new_name = description.replace("-", "_")

        alnum_parts = [as_alnum(x.strip().lower()) for x in new_name.split()]

        # Prune some words if the description is very long.
        if len(alnum_parts) > 1:
            alnum_parts = list(filter(is_name_part, alnum_parts))

        assert alnum_parts, (name, description)

        new_name = "_".join(alnum_parts)

        assert new_name, (name, description)
        name = new_name

    return name


def translate_enums(enum: EnumeratedValues) -> EnumValues:
    """Generate an enumeration definition."""

    result: dict[str, Any] = {}
    enum.handle_description(result)

    for name, value in enum.derived_elem.enum.items():
        enum_data: dict[str, Any] = {}
        value.handle_description(enum_data)

        value_str: str = value.raw_data["value"]

        prefix = ""
        for possible_prefix in ("#", "0b", "0x"):
            if value_str.startswith(possible_prefix):
                prefix = possible_prefix
                break

        if prefix in ("#", "0b"):
            enum_data["value"] = int(
                value_str[len(prefix) :].replace("X", "1"), 2
            )
        elif prefix == "0x":
            enum_data["value"] = int(value_str[len(prefix) :], 16)
        else:
            enum_data["value"] = int(value_str)

        final_name = handle_enum_name(name, value.raw_data.get("description"))
        assert final_name

        # Truncate.
        final_name = (
            final_name if len(final_name) < 51 else final_name[:45] + "_cont"
        )
        assert len(final_name) < 51

        while final_name in result:
            final_name += "_"

        assert final_name not in result, (name, final_name)
        result[final_name] = enum_data

    # Remove common prefix (if present) from enums.
    length = len(commonprefix(list(result)))
    if length > 1:
        result = {
            key[length:] if length < len(key) else key: value
            for key, value in result.items()
        }

    return result
