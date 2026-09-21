"""Every reference in the examples resolves to an id in the document it points at.

A reference slot renders as a plain string in JSON Schema, so linkml-validate accepts
any value there and never sees the document the id lives in. This test is the check that
makes those references type safe in this repository; the generator carries the same rule
at tier 2 (SPEC-common.md decision 17).

Domain modules add rows to REFERENCES and nothing else. A row is
    (document, slot) -> (target document, empty allowed)
Every value found under the slot's key anywhere in the document, lists flattened, must be
the id of a record in the target document; "" passes only where the owning spec says the
key may be empty.
"""
from pathlib import Path

import pytest
import yaml

REFERENCES: dict[tuple[str, str], tuple[str, bool]] = {
    ("examples/process/catalogue.yaml", "requires"): ("examples/common/capability_types.yaml", False),
    ("examples/resource/robot_units.yaml", "offers"): ("examples/common/capability_types.yaml", False),
    ("examples/process/catalogue.yaml", "applies_to"): ("examples/common/material_categories.yaml", False),
    ("examples/product/materials.yaml", "category"): ("examples/common/material_categories.yaml", True),
    ("examples/product/building_components.yaml", "made_of"): ("examples/product/materials.yaml", True),
    ("examples/product/connectors.yaml", "made_of"): ("examples/product/materials.yaml", True),
}


def values_under(node, key: str) -> list:
    """Every value stored under `key` anywhere in node, lists flattened, nesting ignored."""
    found: list = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key:
                found += v if isinstance(v, list) else [v]
            else:
                found += values_under(v, key)
    elif isinstance(node, list):
        for item in node:
            found += values_under(item, key)
    return found


def unresolved(document: Path, slot: str, target: Path, empty_allowed: bool) -> list:
    """The values under `slot` in document that are not an id in target."""
    ids = {record["id"] for record in yaml.safe_load(target.read_text(encoding="utf-8"))}
    values = values_under(yaml.safe_load(document.read_text(encoding="utf-8")), slot)
    return [v for v in values if not (v == "" and empty_allowed) and v not in ids]


@pytest.mark.parametrize(("document", "slot"), sorted(REFERENCES))
def test_reference(root: Path, document: str, slot: str) -> None:
    target, empty_allowed = REFERENCES[(document, slot)]
    bad = unresolved(root / document, slot, root / target, empty_allowed)
    assert not bad, f"{document}: {slot} values {bad} are not ids in {target}"
