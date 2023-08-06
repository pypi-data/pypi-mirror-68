import abc
import json
import subprocess
from pathlib import Path
from typing import List, Optional, Dict


class AbstractOPClient(abc.ABC):
    @abc.abstractmethod
    def sign_in(self, domain: str, email: str) -> None:
        ...

    @abc.abstractmethod
    def login_to_domain(self, domain: str) -> str:
        ...

    @abc.abstractmethod
    def get_password(self, item_name: str) -> str:
        ...


class OPClient(AbstractOPClient):
    def get_password(self, item_name: str) -> str:
        output = (
            subprocess.check_output(
                [str(self.__executable_path), "get", "item", item_name]
            )
            .decode("utf-8")
            .strip()
        )
        return json.loads(output)["details"]["password"]

    def login_to_domain(self, domain: str) -> str:
        return (
            subprocess.check_output(
                [str(self.__executable_path), "signin", domain, "--output=raw"]
            )
            .decode("utf-8")
            .strip()
        )

    def __init__(self, executable_path: Path) -> None:
        self.__executable_path = executable_path

    def sign_in(self, domain: str, email: str) -> None:
        subprocess.check_call(
            [str(self.__executable_path), "signin", domain, email, "--output=raw"]
        )


def find_executable_in_directories(directories: List[Path]) -> Optional[Path]:
    for directory in directories:
        possible_path = directory / "op"
        if possible_path.is_file():
            return possible_path

    return None


def find_executable_in_env(env: Dict[str, str]) -> Optional[Path]:
    return find_executable_in_directories(
        [Path(p) for p in env.get("PATH", "").split(":")]
    )
