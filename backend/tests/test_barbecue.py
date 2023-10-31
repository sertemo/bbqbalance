import pytest
from backend.balance import Barbecue

async def test_add_participant() -> None:
    bbq = Barbecue()
    participant = {
        'name': 'Sergio',
        'initial_expense': 17.56,
        'concepto': "Chucherías"
    }
    await bbq.add_participant(
        **participant

    )
    assert bbq.participants["Sergio"].name == "Sergio"
    assert bbq.participants["Sergio"].initial_expense == 17.56