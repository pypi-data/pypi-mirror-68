from logging import Logger
from pathlib import Path
from typing import Any, Callable

import pytest

from op_askpass.one_password.client import AbstractOPClient
from op_askpass.one_password.downloader import HTTPDownloader
from op_askpass.one_password.file_verifier import GPGFileVerifier
from op_askpass.operations import setup_op_client


class MockOPClient(AbstractOPClient):
    def login_to_domain(self, domain: str) -> str:
        pass

    def get_password(self, item_name: str) -> str:
        pass

    def sign_in(self, domain: str, email: str) -> None:
        pass


@pytest.mark.integration
def test_with_mocked_client_should_correctly_create_binary(
    tmp_path: Path, when: Callable[[Any], Any], null_logger: Logger
) -> None:
    op_client = MockOPClient()
    when(op_client).sign_in(domain="some-domain", email="some-email")

    setup_op_client(
        download_url="https://cache.agilebits.com/dist/1P/op/pkg/v0.5.7/op_linux_amd64_v0.5.7.zip",
        install_path=tmp_path,
        op_domain="some-domain",
        op_email="some-email",
        logger=null_logger,
        verifier=GPGFileVerifier(logger=null_logger),
        downloader=HTTPDownloader(logger=null_logger),
        op_client=op_client,
    )

    executable_path = tmp_path / "op"
    assert oct(executable_path.stat().st_mode & 0o777) == oct(0o755)
