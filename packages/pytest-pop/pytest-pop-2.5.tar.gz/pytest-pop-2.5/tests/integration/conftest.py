import pytest


@pytest.fixture(scope="session")
def hub(hub):
    # TODO Add dynes that will be used for your tests
    for dyne in ():
        hub.pop.sub.add(dyne_name=dyne)
    return hub
