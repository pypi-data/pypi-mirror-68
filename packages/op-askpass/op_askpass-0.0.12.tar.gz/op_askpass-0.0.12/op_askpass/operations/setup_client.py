import shutil
import tempfile
from logging import Logger
from pathlib import Path
from typing import Optional

from op_askpass.one_password.client import AbstractOPClient, OPClient
from op_askpass.one_password.downloader import AbstractDownloader, HTTPDownloader
from op_askpass.one_password.file_verifier import AbstractFileVerifier


def setup_op_client(
    download_url: str,
    install_path: Path,
    op_domain: str,
    op_email: str,
    logger: Logger,
    verifier: Optional[AbstractFileVerifier] = None,
    downloader: AbstractDownloader = None,
    op_client: Optional[AbstractOPClient] = None,
) -> None:
    downloader = downloader or HTTPDownloader(logger=logger)

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(str(tmpdir))
        download_dir = tmpdir / "downloaded_client"
        download_dir.mkdir()
        downloader.download_from_url(url=download_url, target_dir=download_dir)

        if verifier:
            verifier.verify_file_signature(
                file_path=download_dir / "op",
                signature=(download_dir / "op.sig").read_bytes(),
            )

        shutil.copy(src=str(download_dir / "op"), dst=str(install_path / "op"))

    op_client = op_client or OPClient(executable_path=install_path / "op")
    op_client.sign_in(domain=op_domain, email=op_email)
