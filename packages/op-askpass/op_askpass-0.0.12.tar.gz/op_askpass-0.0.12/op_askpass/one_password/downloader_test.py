import abc
from logging import Logger
from pathlib import Path
from stat import S_IEXEC, S_IRUSR, S_IWUSR, S_IRGRP, S_IROTH

import pytest

from op_askpass.one_password.downloader import (
    AbstractDownloader,
    SimpleDownloader,
    HTTPDownloader,
)

TEST_COMMIT_HASH = "027273ecb987e86958c19987a711c9bc0df83c64"


class AbstractDownloaderTests(abc.ABC):
    @abc.abstractmethod
    def downloader_factory(self, logger: Logger) -> AbstractDownloader:
        ...

    def test_download_from_url_should_download_to_given_path(
        self, tmp_path: Path, null_logger: Logger
    ) -> None:
        downloader = self.downloader_factory(logger=null_logger)

        downloader.download_from_url(
            url="https://cache.agilebits.com/dist/1P/op/pkg/v0.5.7/op_linux_amd64_v0.5.7.zip",
            target_dir=tmp_path,
        )

        assert (tmp_path / "op").exists()


class TestSimpleDownloader(AbstractDownloaderTests):
    def downloader_factory(self, logger: Logger) -> AbstractDownloader:
        return SimpleDownloader(files={"op": b"some content"})


@pytest.mark.integration
class TestHTTPDownloader(AbstractDownloaderTests):
    def downloader_factory(self, logger: Logger) -> AbstractDownloader:
        return HTTPDownloader(logger=logger)

    def test_download_from_url_should_download_to_given_path(
        self, tmp_path: Path, null_logger: Logger
    ) -> None:
        expected_mode = S_IEXEC | S_IRUSR | S_IWUSR | S_IRGRP | S_IROTH

        super().test_download_from_url_should_download_to_given_path(
            tmp_path=tmp_path, null_logger=null_logger
        )

        assert (tmp_path / "op").stat().st_mode & expected_mode == expected_mode
