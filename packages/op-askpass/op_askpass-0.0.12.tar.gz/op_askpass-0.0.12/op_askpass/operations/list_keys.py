from typing import List, Tuple

from op_askpass.key_store import AbstractKeyStore


def list_keys(key_store: AbstractKeyStore) -> List[Tuple[str, str]]:
    return [
        (
            f"{fingerprint.length} {fingerprint.hash} {fingerprint.comment} ({fingerprint.key_type})",
            key_entry.onepass_uid,
        )
        for fingerprint, key_entry in key_store.items()
    ]
