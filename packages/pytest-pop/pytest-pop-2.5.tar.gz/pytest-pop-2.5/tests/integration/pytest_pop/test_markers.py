import pytest
import subprocess
import sys
import tempfile

TMP_TEST = """
import pytest
@pytest.mark.{marker}
def test_{marker}():
    pass
"""


@pytest.mark.root
def test_root():
    pass


def test_expensive():
    with tempfile.NamedTemporaryFile("w", prefix="test_", suffix=".py") as tmp:
        tmp.write(TMP_TEST.format(marker="expensive"))
        tmp.flush()
        ret = subprocess.check_output(
            [sys.executable, "-m", "pytest", tmp.name, f"--expensive"]
        )
        assert "1 passed" in ret.decode()


def test_expensive_skip():
    with tempfile.NamedTemporaryFile("w", prefix="test_", suffix=".py") as tmp:
        tmp.write(TMP_TEST.format(marker="expensive"))
        tmp.flush()
        ret = subprocess.check_output([sys.executable, "-m", "pytest", tmp.name])
        assert "1 skipped" in ret.decode()


def test_destructive():
    with tempfile.NamedTemporaryFile("w", prefix="test_", suffix=".py") as tmp:
        tmp.write(TMP_TEST.format(marker="destructive"))
        tmp.flush()
        ret = subprocess.check_output(
            [sys.executable, "-m", "pytest", tmp.name, f"--destructive"]
        )
        assert "1 passed" in ret.decode()


def test_destructive_skip():
    with tempfile.NamedTemporaryFile("w", prefix="test_", suffix=".py") as tmp:
        tmp.write(TMP_TEST.format(marker="destructive"))
        tmp.flush()
        ret = subprocess.check_output([sys.executable, "-m", "pytest", tmp.name])
        assert "1 skipped" in ret.decode()


def test_slow():
    with tempfile.NamedTemporaryFile("w", prefix="test_", suffix=".py") as tmp:
        tmp.write(TMP_TEST.format(marker="slow"))
        tmp.flush()
        ret = subprocess.check_output(
            [sys.executable, "-m", "pytest", tmp.name, f"--slow"]
        )
        assert "1 passed" in ret.decode()


def test_slow_skip():
    with tempfile.NamedTemporaryFile("w", prefix="test_", suffix=".py") as tmp:
        tmp.write(TMP_TEST.format(marker="slow"))
        tmp.flush()
        ret = subprocess.check_output([sys.executable, "-m", "pytest", tmp.name])
        assert "1 skipped" in ret.decode()
