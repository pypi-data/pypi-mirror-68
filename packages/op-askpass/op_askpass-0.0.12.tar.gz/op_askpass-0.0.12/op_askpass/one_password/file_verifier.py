import abc
import hashlib
import subprocess
import tempfile
from logging import Logger
from pathlib import Path


class VerificationError(Exception):
    pass


class AbstractFileVerifier(abc.ABC):
    @abc.abstractmethod
    def verify_file_signature(self, file_path: Path, signature: bytes) -> None:
        ...


class MD5FileVerifier(AbstractFileVerifier):
    def verify_file_signature(self, file_path: Path, signature: bytes) -> None:
        md5 = hashlib.md5()
        with file_path.open(mode="rb") as f:
            for chunk in f:
                md5.update(chunk)

        if md5.hexdigest() != signature.decode("utf-8"):
            raise VerificationError("Wrong signature.")


class GPGFileVerifier(AbstractFileVerifier):
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger

    def verify_file_signature(self, file_path: Path, signature: bytes) -> None:
        self.__logger.info("Verifying GPG signature: %s", file_path)

        with tempfile.NamedTemporaryFile() as tmp:
            tmp_path = Path(tmp.name)
            tmp_path.write_bytes(signature)

            try:
                subprocess.check_call(
                    ["gpg", "--verify", str(tmp_path), str(file_path)]
                )

            except subprocess.CalledProcessError as e:
                raise VerificationError("Wrong signature.") from e
