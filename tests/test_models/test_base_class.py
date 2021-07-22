import pytest
from models.base_class import FileClass


def test_always_passes():
    assert True

@pytest.fixture
def test_allow_file(name_file, object1):
    name_file = "validProfile_word.docx"
    with open("../test_examples/validProfile_word.docx", "rb" ) as file:
        object1 = FileClass(name_file, file)
    allowed = object1.allowed_file()
    assert allowed





