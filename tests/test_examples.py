"""Every example document validates against its class; every invalid one fails naming the slot.

Domain modules add rows to EXAMPLES and nothing else. A row is
    path -> (schema, target class, expected error slot or None)
where None means the document must validate and a slot name means it must fail
with that slot in the error message. A target class of BY_RECORD_TYPE means the
file holds records of several classes: each record is validated against the
class its record_type names, and a record without one fails the row.
"""
from pathlib import Path
import subprocess
import tempfile

import pytest
import yaml

BY_RECORD_TYPE = "by record_type"

EXAMPLES: dict[str, tuple[str, str, str | None]] = {
    "tests/fixtures/minimal_instances.yaml": ("tests/fixtures/minimal.yaml", "Widget", None),
    "tests/fixtures/minimal_invalid.yaml": ("tests/fixtures/minimal.yaml", "Widget", "made_of"),
    "examples/common/capability_types.yaml": ("schema/common.yaml", "CapabilityType", None),
    "examples/common/invalid/capability_type_missing_id.yaml": ("schema/common.yaml", "CapabilityType", "id"),
    "examples/resource/robot_units.yaml": ("schema/resource.yaml", "RobotUnit", None),
    "examples/resource/invalid/robot_unit_missing_activity.yaml": ("schema/resource.yaml", "RobotUnit", "activity_group"),
    "examples/resource/invalid/robot_unit_zero_count.yaml": ("schema/resource.yaml", "RobotUnit", "count"),
    "examples/resource/invalid/activity_missing_offers.yaml": ("schema/resource.yaml", "RobotUnit", "offers"),
    "examples/resource/invalid/robot_unit_group_missing_id.yaml": ("schema/resource.yaml", "RobotUnit", "id"),
    "examples/product/storeys.yaml": ("schema/product.yaml", "Storey", None),
    "examples/product/spaces.yaml": ("schema/product.yaml", "Space", None),
    "examples/product/invalid/space_missing_source.yaml": ("schema/product.yaml", "Space", "source"),
    "examples/product/invalid/space_record_type_mismatch.yaml": ("schema/product.yaml", "Space", "record_type"),
    "examples/product/invalid/storey_id_not_global_id.yaml": ("schema/product.yaml", "Storey", "id"),
    "examples/product/building_components.yaml": ("schema/product.yaml", "BuildingComponent", None),
    "examples/product/invalid/building_component_missing_permanence.yaml": ("schema/product.yaml", "BuildingComponent", "permanence"),
    "examples/product/invalid/building_component_id_not_global_id.yaml": ("schema/product.yaml", "BuildingComponent", "id"),
    "examples/product/invalid/building_component_ifc_missing_ifc_type.yaml": ("schema/product.yaml", "BuildingComponent", "ifc_type"),
    "examples/product/invalid/building_component_derived_missing_derived_from.yaml": ("schema/product.yaml", "BuildingComponent", "derived_from"),
    "examples/product/invalid/building_component_derived_from_empty.yaml": ("schema/product.yaml", "BuildingComponent", "derived_from"),
    "examples/product/connectors.yaml": ("schema/product.yaml", "Connector", None),
    "examples/product/invalid/connector_one_space.yaml": ("schema/product.yaml", "Connector", "connects"),
    "examples/product/invalid/connector_door_missing_clear_height.yaml": ("schema/product.yaml", "Connector", "clear_height"),
    "examples/product/materials.yaml": ("schema/product.yaml", "Material", None),
    "examples/product/invalid/material_missing_category.yaml": ("schema/product.yaml", "Material", "category"),
    "examples/process/catalogue.yaml": ("schema/process.yaml", BY_RECORD_TYPE, None),
    "examples/process/invalid/primitive_task_missing_duration.yaml": ("schema/process.yaml", "PrimitiveTask", "duration"),
    "examples/process/invalid/primitive_task_requires_empty.yaml": ("schema/process.yaml", "PrimitiveTask", "requires"),
    "examples/process/invalid/primitive_task_id_not_a_name.yaml": ("schema/process.yaml", "PrimitiveTask", "id"),
    "examples/process/invalid/primitive_task_parameter_unknown_kind.yaml": ("schema/process.yaml", "PrimitiveTask", "parameters"),
    "examples/process/invalid/compound_task_record_type_mismatch.yaml": ("schema/process.yaml", "CompoundTask", "record_type"),
    "examples/process/invalid/method_parameter_missing_kind.yaml": ("schema/process.yaml", "Method", "parameter_kind"),
    "examples/process/invalid/method_subtask_names_two_tasks.yaml": ("schema/process.yaml", "Method", "subtasks"),
    "examples/process/invalid/method_subtasks_empty.yaml": ("schema/process.yaml", "Method", "subtasks"),
    "examples/process/invalid/method_ordering_not_a_list.yaml": ("schema/process.yaml", "Method", "ordering"),
}


def validate(root: Path, schema: str, target: str, document: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["linkml-validate", "-s", str(root / schema), "-C", target, str(root / document)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def validate_by_record_type(root: Path, schema: str, document: str) -> tuple[int, str]:
    """Split a mixed file into one temporary file per record_type and validate each."""
    records = yaml.safe_load((root / document).read_text(encoding="utf-8"))
    groups: dict[str, list[dict]] = {}
    for n, record in enumerate(records, 1):
        record_type = record.get("record_type") if isinstance(record, dict) else None
        if not record_type:
            return 1, f"record {n} (id: {record.get('id', '?') if isinstance(record, dict) else '?'}) has no record_type"
        groups.setdefault(record_type, []).append(record)
    returncode, output = 0, ""
    with tempfile.TemporaryDirectory() as tmp:
        for record_type, group in groups.items():
            part = Path(tmp) / f"{record_type}.yaml"
            part.write_text(yaml.safe_dump(group, sort_keys=False), encoding="utf-8")
            result = validate(root, schema, record_type, str(part))
            returncode |= result.returncode
            if result.returncode:
                ids = ", ".join(str(r.get("id", "?")) for r in group)
                output += f"record_type {record_type} (records: {ids}):\n"
            output += result.stdout + result.stderr
    return returncode, output


@pytest.mark.parametrize("document", sorted(EXAMPLES))
def test_example(root: Path, document: str) -> None:
    schema, target, expected_error_slot = EXAMPLES[document]
    if target == BY_RECORD_TYPE:
        returncode, output = validate_by_record_type(root, schema, document)
    else:
        result = validate(root, schema, target, document)
        returncode, output = result.returncode, result.stdout + result.stderr
    if expected_error_slot is None:
        assert returncode == 0, output
    else:
        assert returncode != 0, "expected validation to fail but it passed"
        assert expected_error_slot in output, output
