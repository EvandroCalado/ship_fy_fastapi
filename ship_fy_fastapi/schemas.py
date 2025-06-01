from datetime import datetime

from pydantic import BaseModel, Field

from ship_fy_fastapi.database.models import ShipmentStatus


class ShipmentCreate(BaseModel):
    content: str = Field(description='Content description')
    weight: float = Field(description='Weight in kilograms', lt=25, ge=1)
    destination: int = Field(description='Postal code')


class ShipmentRead(ShipmentCreate):
    id: int = Field(description='Shipment id')
    status: ShipmentStatus = Field(description='Shipment status')
    estimated_delivery: datetime = Field(description='Estimated delivery date')


class ShipmentUpdate(BaseModel):
    estimated_delivery: datetime | None = Field(
        description='Estimated delivery date', default=None
    )
    status: ShipmentStatus | None = Field(
        description='Shipment status ',
        default=None,
    )
