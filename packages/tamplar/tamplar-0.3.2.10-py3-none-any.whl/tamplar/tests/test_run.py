import os

import pytest

from tamplar import tests
from tamplar.api import methods
from tamplar.tests import utils


def test_run_full():
    methods.run(src_path=tests.root)
