import pytest
from main import app
from .helper import process_query

@pytest.mark.asyncio
async def test_items_by_client():
    query = '{ itemsByClient(idCliCliente: 8) { descGaSkuProducto } }'
    response = await process_query(query)
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json["itemsByClient"]) > 0
    assert response_json["itemsByClient"][0]["descGaSkuProducto"] is not None
