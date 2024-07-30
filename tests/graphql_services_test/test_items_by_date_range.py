import pytest
from main import app
from .helper import process_query

@pytest.mark.asyncio
async def test_items_by_date_range():
    query = '{ itemsByDateRange(startDate: "20240101", endDate: "20240131") { descGaSkuProducto } }'
    response = await process_query(query)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["itemsByDateRange"]) > 0
    assert response_json["itemsByDateRange"][0]["descGaSkuProducto"] is not None
