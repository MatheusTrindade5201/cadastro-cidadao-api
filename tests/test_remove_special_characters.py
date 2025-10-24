import pytest
from utils.helpers.shared_helpers.remove_special_characters import remove_special_characters

@pytest.mark.parametrize('raw_input,expected', [
    ('123.456-789/000', '123456789000'),
    ('  123.456-789/000  ', '123456789000'),
    ('abc.def-ghi/jkl', 'abcdefghijkl'),
    ('---...///', ''),
    ('', ''),
    ('semcaracteres', 'semcaracteres'),
    ('  semcaracteres  ', 'semcaracteres'),
])
def test_remove_special_characters_basic(raw_input, expected):
    assert remove_special_characters(raw_input) == expected

# Testa comportamento com None e tipos não-string
@pytest.mark.parametrize('raw_input', [None, 12345, 12.34, ['1-2/3.4'], {'a': 'b'}])
def test_remove_special_characters_invalid_type(raw_input):
    with pytest.raises(TypeError):
        remove_special_characters(raw_input)

