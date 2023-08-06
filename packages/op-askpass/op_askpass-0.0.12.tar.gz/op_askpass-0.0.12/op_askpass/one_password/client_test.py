from pathlib import Path

import pytest

from op_askpass.one_password.client import find_executable_in_directories


@pytest.mark.integration
def test_find_executable_in_dirs(tmp_path: Path) -> None:
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    client_dir = tmp_path / "contains"
    client_dir.mkdir()
    (client_dir / "op").write_bytes(b"test")
    without_client_dir = tmp_path / "no_client"
    without_client_dir.mkdir()
    (without_client_dir / "something.txt").write_text("test")

    assert (
        find_executable_in_directories([empty_dir, client_dir, without_client_dir])
        == client_dir / "op"
    )
