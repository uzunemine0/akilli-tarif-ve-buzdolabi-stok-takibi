from datetime import date, timedelta
from src.infrastructure.database import SessionLocal, init_db
from src.domain.models import FridgeItem, Recipe, RecipeIngredient, SavingsLog


def seed_data():
    init_db()
    db = SessionLocal()

    try:
        if db.query(FridgeItem).first():
            print("Veritabaninda zaten ornek veriler mevcut.")
            return

        today = date.today()

        # 1. Buzdolabı Ürünleri (Farklı SKT risk seviyelerinde)
        items = [
            FridgeItem(
                name="Tam Yağlı Süt",
                category="Süt Ürünleri",
                quantity=1.0,
                unit="litre",
                price_tl=38.50,
                expiration_date=today + timedelta(days=1),
                is_consumed=False,
                is_wasted=False,
            ),
            FridgeItem(
                name="Tavuk Göğsü",
                category="Et/Tavuk",
                quantity=500.0,
                unit="gram",
                price_tl=115.00,
                expiration_date=today + timedelta(days=2),
                is_consumed=False,
                is_wasted=False,
            ),
            FridgeItem(
                name="Süzme Yoğurt",
                category="Süt Ürünleri",
                quantity=400.0,
                unit="gram",
                price_tl=55.00,
                expiration_date=today + timedelta(days=3),
                is_consumed=False,
                is_wasted=False,
            ),
            FridgeItem(
                name="Domates",
                category="Sebze/Meyve",
                quantity=4.0,
                unit="adet",
                price_tl=30.00,
                expiration_date=today + timedelta(days=5),
                is_consumed=False,
                is_wasted=False,
            ),
            FridgeItem(
                name="Yumurta",
                category="Kahvaltılık",
                quantity=10.0,
                unit="adet",
                price_tl=65.00,
                expiration_date=today + timedelta(days=12),
                is_consumed=False,
                is_wasted=False,
            ),
        ]
        db.add_all(items)

        # 2. Örnek Tarif ve Malzemeleri
        recipe = Recipe(
            title="Yoğurt Soslu Tavuk Sote",
            prep_time_minutes=25,
            diet_tag="Yüksek Protein",
            instructions="1. Tavuk göğsünü küp doğrayın. 2. Yoğurt ve baharatlarla marine edip tavada 15 dakika soteleyin. 3. Doğranmış domateslerle servis edin.",
        )
        db.add(recipe)
        db.flush()

        ingredients = [
            RecipeIngredient(recipe_id=recipe.id, ingredient_name="Tavuk Göğsü", required_quantity=300.0, unit="gram"),
            RecipeIngredient(recipe_id=recipe.id, ingredient_name="Süzme Yoğurt", required_quantity=150.0, unit="gram"),
            RecipeIngredient(recipe_id=recipe.id, ingredient_name="Domates", required_quantity=2.0, unit="adet"),
        ]
        db.add_all(ingredients)

        # 3. Örnek Tasarruf Kaydı
        sample_saving = SavingsLog(
            recipe_title="Sebzeli Omlet",
            saved_items_count=3,
            saved_amount_tl=72.50,
        )
        db.add(sample_saving)

        db.commit()
        print("Ornek urunler, tarif ve tasarruf verileri basariyla eklendi!")

    finally:
        db.close()


if __name__ == "__main__":
    seed_data()