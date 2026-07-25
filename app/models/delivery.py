from datetime import datetime

from enum import Enum as PyEnum
from sqlalchemy import Enum as SQLEnum

from sqlalchemy import DateTime, String, func, ForeignKey
from uuid import UUID as PyUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base



class DeliveryStatus(str, PyEnum):
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed" 
    
class Delivery(Base):
    __tablename__ = "deliveries"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    
    event_id: Mapped[PyUUID] = mapped_column(ForeignKey("events.id"))
    
    endpoint_id: Mapped[int] = mapped_column(ForeignKey("webhook_endpoints.id"))
    
    status: Mapped[DeliveryStatus] = mapped_column(
        SQLEnum(DeliveryStatus),
        default=DeliveryStatus.PENDING
    )
    
    attempt_count: Mapped[int] = mapped_column(default=0)
    
    last_error: Mapped[str | None] = mapped_column(
        String(500), 
        nullable=True
    )   
    
    next_retry_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    
    event : Mapped["Event"] = relationship(
        back_populates="deliveries"
    )
    
    endpoint: Mapped["WebhookEndpoint"] = relationship(
        back_populates="deliveries"
    )
    
    attempts: Mapped[list["DeliveryAttempt"]] = relationship(
        back_populates= "delivery",
        cascade="all, delete-orphan",
    )