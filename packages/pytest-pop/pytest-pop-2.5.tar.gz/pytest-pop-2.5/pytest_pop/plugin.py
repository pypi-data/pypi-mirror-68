# -*- coding: utf-8 -*-
import _pytest.config as conf
import _pytest.config.argparsing as argparsing
import _pytest.python as pytesthon
import ctypes
import mock
import os
import pop.hub
import pytest
from typing import List


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session: pytest.Session):
    """
    Initialize the hub and attach it to the pytest config
    """
    config: conf.Config = session.config
    config.hub = pop.hub.Hub()
    with mock.patch("sys.argv", ["pytest_pop"]):
        # At the very least set up logging
        config.hub.pop.config.load(["pytest_pop"], "pytest_pop", parse_cli=True)


def pytest_addoption(parser: argparsing.Parser):
    group = parser.getgroup("pytest-pop", "Helpers for testing pop projects")
    group.addoption("--destructive", action="store_true", help="Run destructive tests")
    group.addoption("--expensive", action="store_true", help="Run expensive tests")
    group.addoption("--slow", action="store_true", help="Run slow tests")


def pytest_configure(config: conf.Config):
    # Mark if a test requires root or admin privileges
    config.addinivalue_line("markers", "root(): Test requires Administrator privileges")
    # Given from flags
    config.addinivalue_line("markers", "destructive(): This test is destructive")
    config.addinivalue_line("markers", "expensive(): This test is expensive")
    config.addinivalue_line("markers", "slow(): This test is slow")


def pytest_collection_modifyitems(config: conf.Config, items: List[pytest.Function]):
    # Skip tests that have unset corresponding cli options
    for flag in ("destructive", "expensive", "slow"):
        skipper = pytest.mark.skip(reason=f"Use --{flag} to enable this test")

        opt = (
            str(getattr(config.hub.OPT.pytest_pop, flag))
            .strip()
            .lower()
            .startswith("t")
        )
        pytest_flag = config.getoption(flag, None)
        if pytest_flag or opt:
            # Do not skip the test for this reason if the flag was specified
            continue
        else:
            for item in items:
                if flag in item.keywords:
                    item.add_marker(skipper)


def pytest_runtest_setup(item: pytest.Function):
    if item.get_closest_marker("root"):
        if hasattr(ctypes, "windll"):
            # We're running on windows
            if not ctypes.windll.shell32.IsUserAnAdmin():
                pytest.skip("Test must be run as an administrator")
        elif os.getuid():
            pytest.skip("Test must be run with root privileges")
        else:
            item.config.hub.log.debug(
                f"Running test {item.name} with elevated privileges"
            )


@pytest.fixture(scope="session", autouse=True)
def hub(pytestconfig):
    """
    provides a full hub that is used as a reference for mock_hub
    This can be extended by creating a hub() fixture in your
    own conftest.py and putting `hub` as it's first parameter
    """
    yield pytestconfig.hub


def pytest_generate_tests(metafunc: pytesthon.Metafunc):
    """
    Inject the hub onto module, function, method, and class setup/teardown functions.
    Every fixture, module, function, and class will now have access to the hub.
    """
    if metafunc.cls is not None:
        metafunc.cls.hub = metafunc.config.hub
    if metafunc.function is not None:
        metafunc.function.hub = metafunc.config.hub
    if metafunc.module is not None:
        metafunc.module.hub = metafunc.config.hub
