import graphene
from fastapi import APIRouter, Request, HTTPException, Depends
from graphene import ObjectType, String, Schema, Field, Int, Float, List
from app.auth_service import jwt_required, oauth2_scheme
import pandas as pd
from pydantic import BaseModel

graphql_endpoint = APIRouter()

data_path = 'data/data.csv'
df = pd.read_csv(data_path)

def _is_right_date_format(date):
    return len(str(date)) == 8 and date.isdigit()

def validate_and_convert_date(date_str):
    if not _is_right_date_format(date_str):
        raise HTTPException(status_code=400, detail="Invalid date format, the correct format is: yyyymmdd")
    try:
        return int(date_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, the correct format is: yyyymmdd")

class ItemType(ObjectType):
    id_tie_fecha_valor = graphene.Int()
    id_cli_cliente = graphene.Int()
    id_ga_vista = graphene.String()
    id_ga_tipo_dispositivo = graphene.String()
    id_ga_fuente_medio = graphene.String()
    desc_ga_sku_producto = graphene.String()
    desc_ga_categoria_producto = graphene.String()
    fc_agregado_carrito_cant = graphene.Int()
    fc_ingreso_producto_monto = graphene.Float()
    fc_retirado_carrito_cant = graphene.Int()
    fc_detalle_producto_cant = graphene.Int()
    fc_producto_cant = graphene.Int()
    desc_ga_nombre_producto = graphene.String()
    fc_visualizaciones_pag_cant = graphene.Int()
    flag_pipol = graphene.Int()
    SASASA = graphene.String()
    id_ga_producto = graphene.String()
    desc_ga_nombre_producto_1 = graphene.String()
    desc_ga_sku_producto_1 = graphene.String()
    desc_ga_marca_producto = graphene.String()
    desc_ga_cod_producto = graphene.String()
    desc_categoria_producto = graphene.String()
    desc_categoria_prod_principal = graphene.String()

    @staticmethod
    def from_row(row):
        def safe_get_str(value):
            return value if pd.notna(value) else ""
        
        def safe_get_int(value):
            return value if pd.notna(value) else None
        
        def safe_get_float(value):
            return value if pd.notna(value) else None
        
        return ItemType(
            id_tie_fecha_valor=safe_get_str(row['id_tie_fecha_valor']),
            id_cli_cliente=safe_get_int(row['id_cli_cliente']),
            id_ga_vista=safe_get_str(row['id_ga_vista']),
            id_ga_tipo_dispositivo=safe_get_str(row['id_ga_tipo_dispositivo']),
            id_ga_fuente_medio=safe_get_str(row['id_ga_fuente_medio']),
            desc_ga_sku_producto=safe_get_str(row['desc_ga_sku_producto']),
            desc_ga_categoria_producto=safe_get_str(row['desc_ga_categoria_producto']),
            fc_agregado_carrito_cant=safe_get_int(row['fc_agregado_carrito_cant']),
            fc_ingreso_producto_monto=safe_get_float(row['fc_ingreso_producto_monto']),
            fc_retirado_carrito_cant=safe_get_int(row['fc_retirado_carrito_cant']),
            fc_detalle_producto_cant=safe_get_int(row['fc_detalle_producto_cant']),
            fc_producto_cant=safe_get_int(row['fc_producto_cant']),
            desc_ga_nombre_producto=safe_get_str(row['desc_ga_nombre_producto']),
            fc_visualizaciones_pag_cant=safe_get_int(row['fc_visualizaciones_pag_cant']),
            flag_pipol=safe_get_int(row['flag_pipol']),
            SASASA=safe_get_str(row['SASASA']),
            id_ga_producto=safe_get_int(row['id_ga_producto']),
            desc_ga_nombre_producto_1=safe_get_str(row['desc_ga_nombre_producto_1']),
            desc_ga_sku_producto_1=safe_get_str(row['desc_ga_sku_producto_1']),
            desc_ga_marca_producto=safe_get_str(row['desc_ga_marca_producto']),
            desc_ga_cod_producto=safe_get_str(row['desc_ga_cod_producto']),
            desc_categoria_producto=safe_get_str(row['desc_categoria_producto']),
            desc_categoria_prod_principal=safe_get_str(row['desc_categoria_prod_principal'])
        )


class Query(ObjectType):
    item = Field(ItemType, id_ga_producto=String())
    items_by_client = List(ItemType, id_cli_cliente=Int())
    items_by_date = List(ItemType, id_tie_fecha_valor=String())
    items_by_source = List(ItemType, id_ga_fuente_medio=String())
    items_by_date_range = List(ItemType, start_date=String(), end_date=String())
    items_by_income_range = List(ItemType, min_income=Float(), max_income=Float())

    def resolve_item(root, info, id_ga_producto):
        try:
            id_ga_producto = int(id_ga_producto)
            result = df[df['id_ga_producto'] == id_ga_producto].iloc[0]
            return ItemType.from_row(result)
        except IndexError:
            raise HTTPException(status_code=404, detail="Item not found")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid id_ga_producto")

    def resolve_items_by_client(root, info, id_cli_cliente):
        results = df[df['id_cli_cliente'] == id_cli_cliente]
        return [ItemType.from_row(row) for _, row in results.iterrows()]

    def resolve_items_by_date(root, info, id_tie_fecha_valor):
        id_tie_fecha_valor = validate_and_convert_date(id_tie_fecha_valor)
        results = df[df['id_tie_fecha_valor'] == id_tie_fecha_valor]
        return [ItemType.from_row(row) for _, row in results.iterrows()]

    def resolve_items_by_source(root, info, id_ga_fuente_medio):
        try:
            id_ga_fuente_medio = int(id_ga_fuente_medio)
            results = df[df['id_ga_fuente_medio'] == id_ga_fuente_medio]
            return [ItemType.from_row(row) for _, row in results.iterrows()]
        except IndexError:
            raise HTTPException(status_code=404, detail="Item not found")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid id_ga_fuente_medio")

    def resolve_items_by_date_range(root, info, start_date, end_date):
        start_date = validate_and_convert_date(start_date)
        end_date = validate_and_convert_date(end_date)
        results = df[(df['id_tie_fecha_valor'] >= start_date) & (df['id_tie_fecha_valor'] <= end_date)]
        return [ItemType.from_row(row) for _, row in results.iterrows()]

    def resolve_items_by_income_range(root, info, min_income, max_income):
        results = df[(df['fc_ingreso_producto_monto'] >= min_income) & (df['fc_ingreso_producto_monto'] <= max_income)]
        return [ItemType.from_row(row) for _, row in results.iterrows()]

schema = Schema(query=Query)

class GraphQLQuery(BaseModel):
    query: str


@graphql_endpoint.post(
    "/",
    summary="Ejecutar consulta GraphQL",
    description="""
    Ejecuta una consulta GraphQL en el servidor.

    **Esquemas disponibles**:

    - `item(id_ga_producto: String)`: Obtiene un item por su ID.
    - `itemsByClient(id_cli_cliente: Int)`: Obtiene todos los items de un cliente.
    - `itemsByDate(id_tie_fecha_valor: String)`: Obtiene todos los items de una fecha.
    - `itemsBySource(id_ga_fuente_medio: String)`: Obtiene todos los items de una fuente.
    - `itemsByDateRange(start_date: String, end_date: String)`: Obtiene todos los items en un rango de fechas.
    - `itemsByIncomeRange(min_income: Float, max_income: Float)`: Obtiene todos los items en un rango de ingresos.
    """,
    responses={
        200: {
            "description": "Respuesta exitosa",
            "content": {
                "application/json": {
                    "example": {
                        "item": {
                            "descGaSkuProducto": "K1010148001"
                        }
                    }
                }
            }
        }
    }
)
@jwt_required
async def graphql_post(request: Request, body: GraphQLQuery, token: str = Depends(oauth2_scheme)):
    response = await schema.execute_async(body.query)
    if response.errors:
        try:
            status_code = response.errors[0].original_error.status_code
            detail = response.errors[0].original_error.detail
        except:
            raise HTTPException(status_code=400, detail=response.errors[0].message) # esto es un error generado por GraphQL , por lo que siempre será 400 en este contexto. (Bad Request)
        
        raise HTTPException(status_code=status_code, detail=detail) 

    return response.data