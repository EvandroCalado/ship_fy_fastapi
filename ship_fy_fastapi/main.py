from fastapi import FastAPI, HTTPException, status
from scalar_fastapi import get_scalar_api_reference

from .database import Database
from .schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)

app = FastAPI()

db = Database()


@app.get('/scalar', include_in_schema=False)
def get_scalar_docs():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title='Scalar API',
    )


@app.post(
    '/shipment',
    status_code=status.HTTP_201_CREATED,
    response_model=ShipmentRead,
)
def create_shipment(shipment: ShipmentCreate):
    result = db.create(shipment)

    return result


# @app.get(
#     '/shipment/latest',
#     status_code=status.HTTP_200_OK,
#     response_model=ShipmentRead,
# )
# def get_latest_shipment():
#     id = max(shipments.keys())
#     return shipments[id]


@app.get(
    '/shipment/{id}',
    status_code=status.HTTP_200_OK,
    response_model=ShipmentRead,
)
def get_shipment(id: int):
    shipments = db.get(id)

    if shipments is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found',
        )

    return shipments


@app.patch(
    '/shipment/{id}',
    status_code=status.HTTP_200_OK,
    response_model=ShipmentRead,
)
def update_shipment(id: int, shipment: ShipmentUpdate):
    shipmentExists = db.get(id)

    if shipmentExists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found',
        )

    shipment = db.update(id, shipment)

    return shipment


@app.delete(
    '/shipment/{id}',
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
def delete_shipment(id: int):
    shipmentExists = db.get(id)

    if shipmentExists is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found',
        )

    db.delete(id)

    return {
        'message': 'Shipment deleted',
    }
