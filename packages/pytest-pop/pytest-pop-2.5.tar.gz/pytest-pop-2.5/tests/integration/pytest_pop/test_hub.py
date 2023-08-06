"""
Verify that the hub is part of everything
"""


def setup_module(module):
    hub = module.hub
    hub.log.debug("Setup module")


def setup_function(function):
    hub = function.hub
    hub.log.debug("Setup function")


def test_function(hub):
    hub.log.debug("test function")


class TestHub:
    @classmethod
    def setup_class(cls):
        hub = cls.hub
        hub.log.debug("Setup class")

    def test_method(self):
        hub = self.hub
        hub.log.debug("test method")

    @classmethod
    def teardown_class(cls):
        hub = cls.hub
        hub.log.debug("Teardown class")


def teardown_function(function):
    hub = function.hub
    hub.log.debug("Teardown function")


def teardown_module(module):
    hub = module.hub
    hub.log.debug("Teardown module")
