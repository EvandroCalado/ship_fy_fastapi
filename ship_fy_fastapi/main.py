from typing import Any

from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

app = FastAPI()

shipments = {
    12701: {'weight': 0.6, 'content': 'glassware', 'status': 'placed'},
    12702: {'weight': 1.2, 'content': 'silverware', 'status': 'in transit'},
    12703: {'weight': 1.5, 'content': 'utensils', 'status': 'delivered'},
    12704: {'weight': 2.0, 'content': 'clothes', 'status': 'in transit'},
    12705: {'weight': 2.5, 'content': 'books', 'status': 'shipped'},
}


@app.get('/scalar', include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title='Scalar API',
    )


@app.get('/shipment/latest')
def get_latest_shipment() -> dict[str, Any]:
    id = max(shipments.keys())
    return shipments[id]


@app.get('/shipment/{id}')
def get_shipment(id: int) -> dict[str, Any]:
    if id not in shipments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found',
        )

    return shipments[id]
