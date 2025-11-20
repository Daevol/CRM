from decimal import Decimal
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import StockItem, StockMovement, StockMovementType, User
from app.schemas.inventory import StockItemCreate, StockMovementCreate
from app.services.audit import AuditService


class InventoryService:
    @staticmethod
    def create_item(db: Session, payload: StockItemCreate, actor: User) -> StockItem:
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
        AuditService.log_action(db, actor, "create_stock_item", "StockItem", item.id, {"sku": payload.sku})
        return item

    @staticmethod
    def record_movement(db: Session, payload: StockMovementCreate, actor: User) -> StockMovement:
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
        AuditService.log_action(
            db,
            actor,
            "record_stock_movement",
            "StockMovement",
            movement.id,
            {"reference": payload.reference, "movement_type": payload.movement_type},
        )
        return movement

    @staticmethod
    def list_items(db: Session):
        return db.query(StockItem).all()

    @staticmethod
    def list_movements(db: Session):
        return db.query(StockMovement).order_by(StockMovement.created_at.desc()).all()
