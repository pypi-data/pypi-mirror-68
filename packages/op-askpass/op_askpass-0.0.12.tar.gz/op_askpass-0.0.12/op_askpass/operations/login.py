from op_askpass.key_loader import AbstractKeyLoader
from op_askpass.key_store import AbstractKeyStore
from op_askpass.one_password.client import AbstractOPClient


def login_to_op(
    op_client: AbstractOPClient,
    op_domain: str,
    key_store: AbstractKeyStore,
    key_loader: AbstractKeyLoader,
    skip_existing: bool = True,
) -> None:
    session_key = op_client.login_to_domain(domain=op_domain)
    loaded_fingerprints = set(key_loader.list_loaded_keys())
    for fingerprint, key_entry in key_store.items():
        if fingerprint in loaded_fingerprints and skip_existing:
            print(f"Skipping key {key_entry.key_path}. Already loaded.")
            continue

        key_loader.load_key(
            key_path=key_entry.key_path,
            op_domain=op_domain,
            op_session_key=session_key,
            op_uid=key_entry.onepass_uid,
        )
