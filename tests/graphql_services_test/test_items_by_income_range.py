import pytest
from main import app
from .helper import process_query

@pytest.mark.asyncio
async def test_items_by_income_range():
    query = '{ itemsByIncomeRange(minIncome: 0.0, maxIncome: 1000.0) { descGaSkuProducto } }'
    response = await process_query(query)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["itemsByIncomeRange"]) > 0
    assert response_json["itemsByIncomeRange"][0]["descGaSkuProducto"] is not None
