from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import StockItem, StockMovement, StockMovementType
from app.schemas.inventory import StockItemCreate, StockMovementCreate


class InventoryService:
    @staticmethod
    def create_item(db: Session, payload: StockItemCreate) -> StockItem:
        item = StockItem(
            name=payload.name,
            sku=payload.sku,
            unit=payload.unit,
            quantity=Decimal(str(payload.quantity)),
            location=payload.location,
        )
        db.add(item)
        db.commit()
        db.refresh(item)
        return item

    @staticmethod
    def record_movement(db: Session, payload: StockMovementCreate) -> StockMovement:
        item = db.query(StockItem).filter_by(id=payload.item_id).first()
        if not item:
            raise HTTPException(status_code=404, detail="Товар не найден")
        quantity = Decimal(str(payload.quantity))
        if payload.movement_type == StockMovementType.OUTBOUND and item.quantity - quantity < 0:
            raise HTTPException(status_code=400, detail="Недостаточно запасов")
        movement = StockMovement(
            item_id=payload.item_id,
            quantity=quantity,
            movement_type=payload.movement_type,
            reference=payload.reference,
        )
        if payload.movement_type == StockMovementType.OUTBOUND:
            item.quantity -= quantity
        else:
            item.quantity += quantity
        db.add(movement)
        db.commit()
        db.refresh(movement)
        return movement

    @staticmethod
    def list_items(db: Session):
        return db.query(StockItem).all()

    @staticmethod
    def list_movements(db: Session):
        return db.query(StockMovement).order_by(StockMovement.created_at.desc()).all()
