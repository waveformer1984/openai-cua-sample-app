import inspect
import pytest

from computers import Computer
from computers.default import *
from computers.contrib import *

default_computers = [
    BrowserbaseBrowser,
    LocalPlaywrightBrowser,
    DockerComputer,
    ScrapybaraBrowser,
    ScrapybaraUbuntu,
]

contrib_computers = []

all_computers = default_computers + contrib_computers

# TODO: migrate to a cleaner solution that allows type-checking (e.g. pydantic?)
required_functions = [
    name
    for name, member in inspect.getmembers(Computer)
    if not name.startswith("__") and inspect.isfunction(member)
]


@pytest.mark.parametrize("computer_class", all_computers, ids=lambda c: c.__name__)
def test_computer_implements_interface(computer_class):
    for func in required_functions:
        assert hasattr(
            computer_class, func
        ), f"{computer_class.__name__} is missing required attribute '{func}'"
