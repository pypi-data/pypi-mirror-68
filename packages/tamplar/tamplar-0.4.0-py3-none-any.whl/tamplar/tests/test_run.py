import pytest

from tamplar import tests
from tamplar.__internal import init
from tamplar.api import methods
from tamplar.tests import test_init, utils


@pytest.fixture(scope='function', autouse=True)
def fixture():
    init.default_pip_conf = f'{tests.src_path}/../pip.conf'
    utils.clean(tests.src_path)
    yield
    utils.clean(tests.src_path)


def test_run_full():
    prj_name = 'prj_name'
    answer = None
    agree = 'y'
    folders = []

    test_init.Core(prj_name=prj_name).run_test(answer=answer, agree=agree, folders=folders)
    methods.run(src_path=tests.src_path, mode='env')
