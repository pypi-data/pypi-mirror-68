import logging
import os
from logging import StreamHandler
from pathlib import Path
from typing import Optional

import click

import op_askpass.operations.login
import op_askpass.operations.setup_client
from op_askpass import operations
from op_askpass.configuration import get_configuration_directory
from op_askpass.fingerprint_generator import SSHKeyGenFingerprintGenerator
from op_askpass.key_loader import SSHKeyLoader
from op_askpass.key_store import get_default_key_store
from op_askpass.one_password.client import OPClient, find_executable_in_env
from op_askpass.one_password.file_verifier import GPGFileVerifier


def setup_logging(verbosity: int = 0) -> logging.Logger:
    logger = logging.getLogger(__name__)
    logger.addHandler(StreamHandler())
    logger.setLevel(logging.INFO if verbosity else logging.WARNING)
    return logger


@click.group()
def main() -> None:
    """Yada yada"""


@main.command()
def list_keys() -> None:
    """ Print already stored keys fingerprint and their 1Password uids. """
    keys = operations.list_keys(key_store=get_default_key_store())
    for fingerprint, onepass_uid in keys:
        print(fingerprint, "||", onepass_uid)


@main.command()
@click.argument("op_domain")
@click.argument("op_email")
@click.option(
    "--install-path", type=Path, help="Where the 1Password client should be installed."
)
@click.option(
    "--verify/--no-verify",
    default=True,
    help="Should the download 1Password client binary be verified.",
)
@click.option("--verbose", "-v", "verbosity", type=int, count=True)
def setup_op_client(
    op_domain: str,
    op_email: str,
    verify: bool,
    install_path: Optional[Path],
    verbosity: int,
) -> None:
    """ Download the 1Password API client and login to email in domain. """
    logger = setup_logging(verbosity=verbosity)

    op_askpass.operations.setup_client.setup_op_client(
        download_url="https://cache.agilebits.com/dist/1P/op/pkg/v0.10.0/op_linux_amd64_v0.10.0.zip",
        install_path=install_path or get_configuration_directory(),
        op_domain=op_domain,
        op_email=op_email,
        logger=logger,
        verifier=GPGFileVerifier(logger=logger) if verify else None,
    )


@main.command()
@click.argument("op_domain")
@click.option(
    "--install-path", type=Path, help="Where the 1Password client was installed."
)
@click.option(
    "--skip-existing/--no-skip-existing",
    default=True,
    help="Skip keys already existing in the ssh agent.",
)
def login(
    op_domain: str, install_path: Optional[Path], skip_existing: bool = True
) -> None:
    if install_path:
        executable_path = install_path / "op"
    else:
        executable_path = (
            find_executable_in_env(os.environ) or get_configuration_directory() / "op"
        )

    op_askpass.operations.login.login_to_op(
        op_client=OPClient(executable_path=executable_path),
        op_domain=op_domain,
        key_store=get_default_key_store(),
        key_loader=SSHKeyLoader(),
        skip_existing=skip_existing,
    )


@main.command()
@click.argument("public_or_private_key", type=Path)
def delete_key(public_or_private_key: Path) -> None:
    """ Remove given key from prompt-less store. """
    operations.delete_key_from_path(
        path=public_or_private_key,
        fingerprint_generator=SSHKeyGenFingerprintGenerator(),
        key_store=get_default_key_store(),
    )


@main.command()
@click.argument("public_or_private_key", type=Path)
@click.argument("onepass_name_or_uid", type=str)
def add_key(public_or_private_key: Path, onepass_name_or_uid: str) -> None:
    """ Add given key with password stored in 1Password. The key will be available later on for prompt-less add. """
    operations.add_key_from_path(
        path=public_or_private_key,
        onepass_uid=onepass_name_or_uid,
        fingerprint_generator=SSHKeyGenFingerprintGenerator(),
        key_store=get_default_key_store(),
    )
