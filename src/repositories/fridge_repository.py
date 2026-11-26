from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session
from src.domain.models import FridgeItem


class FridgeRepository:
    """Buzdolabı ürünleri (FridgeItem) için veritabanı ekleme, listeleme ve silme sorgularını yönetir."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def add_item(
        self,
        name: str,
        category: str,
        quantity: float,
        unit: str,
        expiration_date: date,
        price_tl: float = 0.0,
    ) -> FridgeItem:
        """Veritabanına yeni bir buzdolabı ürünü ekler."""
        new_item = FridgeItem(
            name=name,
            category=category,
            quantity=quantity,
            unit=unit,
            price_tl=price_tl,
            expiration_date=expiration_date,
        )
        self.db.add(new_item)
        self.db.commit()
        self.db.refresh(new_item)
        return new_item

    def get_all_items(self) -> List[FridgeItem]:
        """Veritabanındaki tüm ürünleri son kullanma tarihine göre sıralı listeler."""
        return (
            self.db.query(FridgeItem)
            .order_by(FridgeItem.expiration_date.asc())
            .all()
        )

    def get_active_items(self) -> List[FridgeItem]:
        """Tüketilmemiş ve israf olmamış aktif buzdolabı ürünlerini listeler."""
        return (
            self.db.query(FridgeItem)
            .filter(
                FridgeItem.is_consumed.is_(False),
                FridgeItem.is_wasted.is_(False),
            )
            .order_by(FridgeItem.expiration_date.asc())
            .all()
        )

    def get_item_by_id(self, item_id: int) -> Optional[FridgeItem]:
        """Verilen ID değerine sahip tek bir ürünü getirir."""
        return (
            self.db.query(FridgeItem)
            .filter(FridgeItem.id == item_id)
            .first()
        )

    def mark_as_consumed(self, item_id: int) -> Optional[FridgeItem]:
        """Ürünü tüketildi olarak işaretler."""
        item = self.get_item_by_id(item_id)
        if not item:
            return None
        item.is_consumed = True
        self.db.commit()
        self.db.refresh(item)
        return item

    def mark_as_wasted(self, item_id: int) -> Optional[FridgeItem]:
        """Ürünü israf oldu olarak işaretler."""
        item = self.get_item_by_id(item_id)
        if not item:
            return None
        item.is_wasted = True
        self.db.commit()
        self.db.refresh(item)
        return item

    def delete_item(self, item_id: int) -> bool:
        """Verilen ID değerine sahip ürünü veritabanından siler."""
        item = self.get_item_by_id(item_id)
        if not item:
            return False
        self.db.delete(item)
        self.db.commit()
        return True
    