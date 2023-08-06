import abc
import os
import tempfile
import zipfile
from logging import Logger
from pathlib import Path
from typing import Dict, Optional

import requests


class AbstractDownloader(abc.ABC):
    @abc.abstractmethod
    def download_from_url(self, url: str, target_dir: Path) -> None:
        ...


class SimpleDownloader(AbstractDownloader):
    def download_from_url(self, url: str, target_dir: Path) -> None:
        for file_path, contents in self.__files.items():
            path_in_target = target_dir / file_path
            path_in_target.parent.mkdir(exist_ok=True)
            (target_dir / file_path).write_bytes(contents)

    def __init__(self, files: Dict[str, bytes]) -> None:
        self.__files = files.copy()


class ZipFileWithPermissions(zipfile.ZipFile):
    def _extract_member(
        self,
        member: Optional[zipfile.ZipInfo],
        targetpath: str,
        pwd: Optional[str] = None,
    ) -> str:
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        targetpath = super()._extract_member(member, targetpath, pwd)

        attr = member.external_attr >> 16
        if attr != 0:
            os.chmod(targetpath, attr)
        return targetpath


class HTTPDownloader(AbstractDownloader):
    def __init__(self, logger: Logger) -> None:
        self.__logger = logger

    def download_from_url(self, url: str, target_dir: Path) -> None:
        self.__logger.info("Fetching: %s", url)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir = Path(tmpdir)
            download_path = tmpdir / "downloaded.zip"
            with open(download_path, "wb") as downloaded_file, requests.get(
                url=url, stream=True
            ) as stream:
                for chunk in stream:
                    downloaded_file.write(chunk)

            with ZipFileWithPermissions(download_path) as archive:
                archive.extractall(path=target_dir)
