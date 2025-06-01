from datetime import datetime, timezone
from enum import Enum

from sqlmodel import Field, SQLModel


class ShipmentStatus(str, Enum):
    placed = 'placed'
    in_transit = 'in_transit'
    shipped = 'shipped'
    delivered = 'delivered'


class Shipment(SQLModel, table=True):
    __tablename__ = 'shipment'

    id: int = Field(default=None, primary_key=True, index=True)
    content: str
    weight: float = Field(le=25, ge=1)
    destination: int
    status: ShipmentStatus
    estimated_delivery: datetime
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
