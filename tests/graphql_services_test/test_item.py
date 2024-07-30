import pytest
from main import app
from .helper import process_query

@pytest.mark.asyncio
async def test_item_correct_int():
    query = '{ item(idGaProducto: "-3637462437398938388") { descGaSkuProducto } }'
    response = await process_query(query)
    assert response.status_code == 200
    response_json = response.json()
    assert response_json["item"]["descGaSkuProducto"] == "K1010148001"

@pytest.mark.asyncio
async def test_item_integer_without_quotes():
    query = '{ item(idGaProducto: -3637462437398938388) { idGaTipoDispositivo } }'
    response = await process_query(query)
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_item_nonexistent_value():
    query = '{ item(idGaProducto: "123123123") { idGaTipoDispositivo } }'
    response = await process_query(query)
    assert response.status_code == 404
