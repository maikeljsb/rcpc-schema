"""Shared pytest fixtures. Nothing here but the repository root."""
from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def root() -> Path:
    return Path(__file__).resolve().parents[1]
