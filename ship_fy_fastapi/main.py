from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import FastAPI, HTTPException, status
from rich import panel, print
from scalar_fastapi import get_scalar_api_reference

from ship_fy_fastapi.database.models import Shipment, ShipmentStatus
from ship_fy_fastapi.database.session import SessionDep, create_db_tables
from ship_fy_fastapi.schemas import (
    ShipmentCreate,
    ShipmentRead,
    ShipmentUpdate,
)


@asynccontextmanager
async def lifespan_handler(app: FastAPI):
    print(panel.Panel('Server started...', border_style='green'))
    create_db_tables()
    yield
    print(panel.Panel('Server stopped...', border_style='red'))


app = FastAPI(lifespan=lifespan_handler)


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
def create_shipment(shipment: ShipmentCreate, session: SessionDep):
    new_shipment = Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )

    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)

    return new_shipment


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
def get_shipment(id: int, session: SessionDep):
    shipments = session.get(Shipment, id)

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
def update_shipment(
    id: int,
    shipment_update: ShipmentUpdate,
    session: SessionDep,
):
    update = shipment_update.model_dump(exclude_unset=True)

    if not update:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='No data provided',
        )

    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found',
        )

    shipment.sqlmodel_update(update)

    session.add(shipment)
    session.commit()
    session.refresh(shipment)

    return shipment


@app.delete(
    '/shipment/{id}',
    status_code=status.HTTP_200_OK,
    response_model=dict,
)
def delete_shipment(id: int, session: SessionDep):
    shipment = session.get(Shipment, id)

    if shipment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Shipment not found',
        )

    session.delete(session.get(Shipment, id))

    session.commit()

    return {
        'message': 'Shipment deleted',
    }
