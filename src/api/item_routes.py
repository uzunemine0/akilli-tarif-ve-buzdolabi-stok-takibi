
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date

from src.infrastructure.database import get_db
from src.domain.models import FridgeItem

router = APIRouter(prefix="/items", tags=["Buzdolabı Ürünleri"])


@router.post("/")
def add_item(
    name: str,
    category: str,
    quantity: float,
    unit: str,
    price_tl: float,
    expiration_date: date,
    db: Session = Depends(get_db)
):
    new_item = FridgeItem(
        name=name,
        category=category,
        quantity=quantity,
        unit=unit,
        price_tl=price_tl,
        expiration_date=expiration_date
    )

    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {
        "message": "Ürün başarıyla eklendi.",
        "item_id": new_item.id,
        "name": new_item.name
    }


@router.get("/")
def list_items(db: Session = Depends(get_db)):
    items = db.query(FridgeItem).all()

    return items


@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(FridgeItem).filter(
        FridgeItem.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Ürün bulunamadı."
        )

    db.delete(item)
    db.commit()

    return {"message": "Ürün başarıyla silindi."}

@router.put("/{item_id}")
def update_item(
    item_id: int,
    name: str = None,
    category: str = None,
    quantity: float = None,
    unit: str = None,
    price_tl: float = None,
    expiration_date: date = None,
    db: Session = Depends(get_db)
):
    item = db.query(FridgeItem).filter(
        FridgeItem.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Ürün bulunamadı."
        )

    if name is not None:
        item.name = name

    if category is not None:
        item.category = category

    if quantity is not None:
        item.quantity = quantity

    if unit is not None:
        item.unit = unit

    if price_tl is not None:
        item.price_tl = price_tl

    if expiration_date is not None:
        item.expiration_date = expiration_date

    db.commit()
    db.refresh(item)

    return {
        "message": "Ürün başarıyla güncellendi.",
        "item_id": item.id,
        "name": item.name,
        "quantity": item.quantity,
        "price_tl": item.price_tl
    }

@router.patch("/{item_id}/consume")
def consume_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(FridgeItem).filter(
        FridgeItem.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Ürün bulunamadı."
        )

    item.is_consumed = True
    item.is_wasted = False

    db.commit()
    db.refresh(item)

    return {
        "message": "Ürün tüketildi olarak işaretlendi.",
        "item_id": item.id,
        "is_consumed": item.is_consumed
    }


@router.patch("/{item_id}/waste")
def waste_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(FridgeItem).filter(
        FridgeItem.id == item_id
    ).first()

    if item is None:
        raise HTTPException(
            status_code=404,
            detail="Ürün bulunamadı."
        )

    item.is_wasted = True
    item.is_consumed = False

    db.commit()
    db.refresh(item)

    return {
        "message": "Ürün israf edildi olarak işaretlendi.",
        "item_id": item.id,
        "is_wasted": item.is_wasted
    }

