**********
PYTEST-POP
**********
**A pytest plugin to help with testing pop projects**

INSTALLATION
============

Install with pip::

    pip install pytest-pop

DEVELOPMENT INSTALLATION
========================


Clone the `pytest-pop` repo and install with pip::

    git clone https://gitlab.com/saltstack/pop/pytest-pop.git
    pip install -e pytest-pop


Getting the Hub
===============

Extend the `hub` fixture in your conftest.py so that it includes your subs::

    # Scoped for session because creating the hub is an expensive process
    @pytest.fixture(scope="session")
    def hub(hub):
        for dyne in ("exec", "states):
            hub.pop.sub.add(dyne_name=dyne)
        yield hub

The full hub you need is now available everywhere in pytest!

In fixtures::

    @pytest.fixture
    def my_fixture(hub):
        hub = hub

In modules::

    def setup_module(module):
        hub = module.hub

    def teardown_module(module):
        hub = module.hub

In functions::

    def setup_function(function):
        hub = function.hub

    def test_func(hub):
        hub = hub

    def teardown_function(function):
        hub = function.hub

In classes::

    class TestClass:
        @classmethod
        def setup_class(cls):
            hub = cls.hub

        def test_method(self):
            hub = self.hub

        @classmethod
        def teardown_class(cls):
            hub = cls.hub

Markers
=======
Make use of pytest's marking functionality


root
----
Marks a test as needing elevated privileges.
On UNIX-like systems the test will be skipped if the user running the tests is not root.
On Windows systems the test will be skipped if the tests aren't run with admin privileges.

Example::

    @pytest.mark.root
    def test_root(hub):
        pass

expensive
---------
Marks a test as being expensive.
Run pytest with the '--expensive' flag or set the `EXPENSIVE_TESTS` environment variable to "True" to run these tests.
By default they will be skipped

Example::

    @pytest.mark.expensive
    def test_expensive(hub):
        pass

destructive
-----------
Marks a test as being destructive.
Run pytest with the '--destructive' flag or set the `DESTRUCTIVE_TESTS` environment variable to "True" to run these tests.
By default they will be skipped

Example::

    @pytest.mark.destructive
    def test_destructive(hub):
        pass

slow
----
Marks a test as being slow.
Run pytest with the '--slow' flag or set the `SLOW_TESTS` environment variable to "True" to run these tests.
By default they will be skipped

Example::

    @pytest.mark.slow
    def test_slow(hub):
        pass

Logging
=======

You can use the hub to log without setting up a logger in every single file

Example::

    hub.log.debug("debug message")


Be sure to run pytest with '--cli-log-level=10' in order to see debug messages

Mocking
=======

Get access to a fully mocked/autospecced version of the hub with::

    mock_hub = hub.pop.testing.mock_hub()


Include a fixture like this one in the conftest.py in the root of your unit test directory::

    # Scope the mock_hub to a function so that the autospec gets reset after each use.
    @pytest.fixture(scope="function")
    def mock_hub(hub):
        mock_hub = hub.pop.testing.mock_hub()
        # replace mocked functions with necessary real ones
        # extend this on a per-module or per-function basis if necessary
        mock_hub.log = hub.log
        yield mock_hub

You can now do autospec assertions on contracted functions::

    import project.sub.plugin as plugin

    def test_cmd_run(mock_hub):
        plugin.func(mock_hub, "arg")
        mock_hub.sub.plugin.func.assert_called_with("arg")

Writing Tests
=============

There's some boiler plate code that may be useful to get you started in this repo's `test` directory.