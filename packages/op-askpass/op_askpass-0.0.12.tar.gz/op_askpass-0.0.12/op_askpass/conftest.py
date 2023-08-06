import logging
from logging import Logger

import pytest


@pytest.fixture
def null_logger() -> Logger:
    logger = logging.getLogger(__name__)
    return logger
