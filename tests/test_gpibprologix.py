import logging

import pytest

from GPIBPrologix import ResourceManager

COMPORT = "COM3"

@pytest.fixture()
def gpib_prologix():
    rm = ResourceManager(COMPORT)
    inst = rm.open_resource(2)
    yield inst
    rm.close()


def test_set_log_level(capsys, gpib_prologix):
    logger = logging.getLogger("GPIBPrologix")
    logger.setLevel(logging.DEBUG)
    data = gpib_prologix.query("*IDN?")
    out, err = capsys.readouterr()
    assert data in out


def test_get_idn(gpib_prologix):
    data = gpib_prologix.query("*IDN?")
    print(data)

