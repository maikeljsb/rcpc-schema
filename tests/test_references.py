"""Every reference in the examples resolves to an id in the document it points at.

A reference slot renders as a plain string in JSON Schema, so linkml-validate accepts
any value there and never sees the document the id lives in. This test is the check that
makes those references type safe in this repository; the generator carries the same rule
at tier 2 (SPEC-common.md decision 17).

Domain modules add rows to REFERENCES and nothing else. A row is
    (document, slot) -> (target documents, empty allowed)
Every value found under the slot's key anywhere in the document, lists flattened and a
keyed map read by its values, must be the id of a record in one of the target documents;
"" passes only where the owning spec says the key may be empty. A record with a count, a
robot entry, stands for its machines <id>_<n> and not for itself; a stock, which also
has a count, stands for itself, because a method names the stock and the export mints
its units.
"""
from pathlib import Path

import pytest
import yaml

CAPABILITIES = ("examples/common/capability_types.yaml",)
CATEGORIES = ("examples/common/material_categories.yaml",)
MATERIALS = ("examples/product/materials.yaml",)
CATALOGUE = ("examples/process/catalogue.yaml",)
STOCKS = ("examples/resource/stocks.yaml",)
PLAN = ("examples/process/plan.yaml",)
OBJECTS = (
    "examples/product/building_components.yaml",
    "examples/product/connectors.yaml",
    "examples/product/spaces.yaml",
    "examples/resource/robot_units.yaml",
)

REFERENCES: dict[tuple[str, str], tuple[tuple[str, ...], bool]] = {
    ("examples/process/catalogue.yaml", "requires"): (CAPABILITIES, False),
    ("examples/resource/robot_units.yaml", "offers"): (CAPABILITIES, False),
    ("examples/process/catalogue.yaml", "applies_to"): (CATEGORIES, False),
    ("examples/process/catalogue.yaml", "uses"): (STOCKS, False),
    ("examples/product/materials.yaml", "category"): (CATEGORIES, True),
    ("examples/product/building_components.yaml", "made_of"): (MATERIALS, True),
    ("examples/product/connectors.yaml", "made_of"): (MATERIALS, True),
    ("examples/process/plan.yaml", "compound_task"): (CATALOGUE, False),
    ("examples/process/plan.yaml", "primitive_task"): (CATALOGUE, False),
    ("examples/process/plan.yaml", "decomposed_by"): (CATALOGUE, True),
    ("examples/process/plan.yaml", "tasks"): (PLAN, False),
    ("examples/process/plan.yaml", "subtasks"): (PLAN, False),
    ("examples/process/plan.yaml", "bindings"): (OBJECTS, False),
}


def values_under(node, key: str) -> list:
    """Every value stored under `key` anywhere in node: lists flattened, a map read by its values."""
    found: list = []
    if isinstance(node, dict):
        for k, v in node.items():
            if k == key:
                found += v if isinstance(v, list) else list(v.values()) if isinstance(v, dict) else [v]
            else:
                found += values_under(v, key)
    elif isinstance(node, list):
        for item in node:
            found += values_under(item, key)
    return found


def ids_in(target: Path) -> set[str]:
    """The ids of target's records; a robot entry stands for its machines <id>_<n>."""
    ids: set[str] = set()
    for record in yaml.safe_load(target.read_text(encoding="utf-8")):
        if "activity_group" in record:
            ids |= {f"{record['id']}_{n}" for n in range(1, record["count"] + 1)}
        else:
            ids.add(record["id"])
    return ids


def unresolved(document: Path, slot: str, targets: list[Path], empty_allowed: bool) -> list:
    """The values under `slot` in document that are not an id in any target."""
    ids = set().union(*(ids_in(target) for target in targets))
    values = values_under(yaml.safe_load(document.read_text(encoding="utf-8")), slot)
    return [v for v in values if not (v == "" and empty_allowed) and v not in ids]


@pytest.mark.parametrize(("document", "slot"), sorted(REFERENCES))
def test_reference(root: Path, document: str, slot: str) -> None:
    targets, empty_allowed = REFERENCES[(document, slot)]
    bad = unresolved(root / document, slot, [root / t for t in targets], empty_allowed)
    assert not bad, f"{document}: {slot} values {bad} are not ids in {', '.join(targets)}"
