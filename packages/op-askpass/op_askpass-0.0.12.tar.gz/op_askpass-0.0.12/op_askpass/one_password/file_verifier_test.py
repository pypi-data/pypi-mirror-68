import abc
from logging import Logger
from pathlib import Path

import pytest

from op_askpass.one_password.file_verifier import (
    AbstractFileVerifier,
    MD5FileVerifier,
    VerificationError,
    GPGFileVerifier,
)


class AbstractBinaryVerifierTests(abc.ABC):
    @abc.abstractmethod
    def get_signature_file_name(self) -> str:
        ...

    @abc.abstractmethod
    def verifier_factory(self, logger: Logger) -> AbstractFileVerifier:
        ...

    def test_verify_file_signature_should_correctly_verify_signature(
        self, null_logger: Logger
    ) -> None:
        verifier: AbstractFileVerifier = self.verifier_factory(logger=null_logger)
        test_data_path = Path(__file__).parent.parent / "test_data"
        key_path = test_data_path / "test_key"
        signature_path = test_data_path / self.get_signature_file_name()

        verifier.verify_file_signature(
            file_path=key_path, signature=signature_path.read_bytes().strip()
        )

    def test_verify_file_signature_should_raise_verification_error_on_incorrect_signature(
        self, null_logger: Logger
    ) -> None:
        verifier: AbstractFileVerifier = self.verifier_factory(logger=null_logger)
        test_data_path = Path(__file__).parent.parent / "test_data"
        key_path = test_data_path / "test_key"

        with pytest.raises(VerificationError, match=r"Wrong signature\."):
            verifier.verify_file_signature(
                file_path=key_path, signature=key_path.read_bytes().strip()
            )


class TestMD5BinaryVerifier(AbstractBinaryVerifierTests):
    def verifier_factory(self, logger: Logger) -> AbstractFileVerifier:
        return MD5FileVerifier()

    def get_signature_file_name(self) -> str:
        return "test_key.md5"


class TestGPGBinaryVerifier(AbstractBinaryVerifierTests):
    def get_signature_file_name(self) -> str:
        return "test_key.sig"

    def verifier_factory(self, logger: Logger) -> AbstractFileVerifier:
        return GPGFileVerifier(logger=logger)
