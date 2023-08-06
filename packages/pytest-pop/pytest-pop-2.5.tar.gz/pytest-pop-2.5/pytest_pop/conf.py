from typing import Any, Dict

CLI_CONFIG: Dict[str, Dict[str, Any]] = {
    "destructive": {},
    "expensive": {},
    "slow": {},
}
CONFIG: Dict[str, Dict[str, Any]] = {
    "destructive": {
        "default": False,
        "os": "DESTRUCTIVE_TESTS",
        "help": "Run destructive tests",
    },
    "expensive": {
        "default": False,
        "help": "Run expensive tests",
        "os": "EXPENSIVE_TESTS",
    },
    "slow": {"default": False, "help": "Run slow tests", "os": "SLOW_TESTS",},
}
