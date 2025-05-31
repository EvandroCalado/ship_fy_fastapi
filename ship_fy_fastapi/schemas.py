from enum import Enum

from pydantic import BaseModel, Field


class ShipmentStatus(str, Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    shipped = 'shipped'
    delivered = 'delivered'


class ShipmentCreate(BaseModel):
    content: str = Field(description='Content description')
    weight: float = Field(description='Weight in kilograms', lt=25, ge=1)
    destination: int = Field(description='Postal code')


class ShipmentRead(ShipmentCreate):
    status: ShipmentStatus = Field(
        description='Shipment status', default=ShipmentStatus.placed
    )


class ShipmentUpdate(BaseModel):
    content: str | None = Field(
        description='Content description', default=None
    )
    weight: float | None = Field(
        description='Weight in kilograms', lt=25, ge=1, default=None
    )
    destination: int | None = Field(description='Postal code', default=None)
    status: ShipmentStatus
