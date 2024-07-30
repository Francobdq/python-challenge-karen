import pytest
from main import app
from .helper import process_query

@pytest.mark.asyncio
async def test_items_by_date():
    query = '{ itemsByDate(idTieFechaValor: "20240129") { descGaSkuProducto } }'
    response = await process_query(query)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["itemsByDate"]) > 0
    assert response_json["itemsByDate"][0]["descGaSkuProducto"] is not None
