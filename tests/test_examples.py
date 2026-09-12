"""Every example document validates against its class; every invalid one fails naming the slot.

Domain modules add rows to EXAMPLES and nothing else. A row is
    path -> (schema, target class, expected error slot or None)
where None means the document must validate and a slot name means it must fail
with that slot in the error message.
"""
from pathlib import Path
import subprocess

import pytest

EXAMPLES: dict[str, tuple[str, str, str | None]] = {
    "tests/fixtures/minimal_instances.yaml": ("tests/fixtures/minimal.yaml", "Widget", None),
    "tests/fixtures/minimal_invalid.yaml": ("tests/fixtures/minimal.yaml", "Widget", "made_of"),
    "examples/common/capability_types.yaml": ("schema/common.yaml", "CapabilityType", None),
    "examples/common/invalid/capability_type_missing_id.yaml": ("schema/common.yaml", "CapabilityType", "id"),
    "examples/resource/robot_units.yaml": ("schema/resource.yaml", "RobotUnit", None),
    "examples/resource/invalid/robot_unit_missing_activity.yaml": ("schema/resource.yaml", "RobotUnit", "activity"),
    "examples/resource/invalid/robot_unit_zero_count.yaml": ("schema/resource.yaml", "RobotUnit", "count"),
    "examples/resource/invalid/activity_missing_offers.yaml": ("schema/resource.yaml", "RobotUnit", "offers"),
}


def validate(root: Path, schema: str, target: str, document: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["linkml-validate", "-s", str(root / schema), "-C", target, str(root / document)],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


@pytest.mark.parametrize("document", sorted(EXAMPLES))
def test_example(root: Path, document: str) -> None:
    schema, target, expected_error_slot = EXAMPLES[document]
    result = validate(root, schema, target, document)
    output = result.stdout + result.stderr
    if expected_error_slot is None:
        assert result.returncode == 0, output
    else:
        assert result.returncode != 0, "expected validation to fail but it passed"
        assert expected_error_slot in output, output
