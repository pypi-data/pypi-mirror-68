import json
import subprocess
from pathlib import Path

__all__ = ["get_password_from_op"]


def get_password_from_op(executable: Path, item_name: str) -> str:
    output = (
        subprocess.check_output([str(executable), "get", "item", item_name])
        .decode("utf-8")
        .strip()
    )
    return json.loads(output)["details"]["password"]
