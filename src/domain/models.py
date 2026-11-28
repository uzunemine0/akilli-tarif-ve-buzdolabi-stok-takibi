from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, Date, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class FridgeItem(Base):
    __tablename__ = "fridge_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)          
    category = Column(String, nullable=False)                  
    quantity = Column(Float, nullable=False)                   
    unit = Column(String, nullable=False)                      
    price_tl = Column(Float, nullable=False, default=0.0)      
    expiration_date = Column(Date, nullable=False)             
    is_consumed = Column(Boolean, default=False)               
    is_wasted = Column(Boolean, default=False)                 
    created_at = Column(DateTime, default=datetime.utcnow)


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)                     
    prep_time_minutes = Column(Integer, nullable=False)        
    diet_tag = Column(String, nullable=True)                   
    instructions = Column(String, nullable=False)            

    ingredients = relationship("RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan")


class RecipeIngredient(Base):
    __tablename__ = "recipe_ingredients"

    id = Column(Integer, primary_key=True, index=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), nullable=False)
    ingredient_name = Column(String, nullable=False)
    required_quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")


class SavingsLog(Base):
    __tablename__ = "savings_logs"

    id = Column(Integer, primary_key=True, index=True)
    recipe_title = Column(String, nullable=False)
    saved_items_count = Column(Integer, nullable=False)        
    saved_amount_tl = Column(Float, nullable=False)            
    logged_at = Column(DateTime, default=datetime.utcnow)

    
