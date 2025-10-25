import pytest
import pytz
from datetime import datetime
from utils.helpers.time_helpers.utc_to_local import utc_to_local

# Testa conversão de UTC para local
@pytest.mark.parametrize('utc_dt,expected', [
    (datetime(2023, 1, 1, 12, 0, 0), datetime(2023, 1, 1, 9, 0, 0)),  # Horário padrão (UTC-3)
    (datetime(2023, 7, 1, 12, 0, 0), datetime(2023, 7, 1, 9, 0, 0)),  # Fora do horário de verão
    (datetime(2023, 1, 1, 0, 0, 0), datetime(2022, 12, 31, 21, 0, 0)), # Virada de dia
])
def test_utc_to_local_basic(utc_dt, expected):
    utc_dt = utc_dt.replace(tzinfo=None)  # Simula entrada sem timezone
    result = utc_to_local(utc_dt)
    assert result == expected

# Testa entrada já com tzinfo UTC
@pytest.mark.parametrize('utc_dt,expected', [
    (datetime(2023, 1, 1, 12, 0, 0, tzinfo=pytz.utc), datetime(2023, 1, 1, 9, 0, 0)),
])
def test_utc_to_local_with_tzinfo(utc_dt, expected):
    result = utc_to_local(utc_dt)
    assert result == expected

# Testa tipos inválidos
@pytest.mark.parametrize('invalid', [None, '2023-01-01T12:00:00', 123456])
def test_utc_to_local_invalid_type(invalid):
    with pytest.raises(TypeError):
        utc_to_local(invalid)
