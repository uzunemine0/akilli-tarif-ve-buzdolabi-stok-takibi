
from fastapi import FastAPI
from src.infrastructure.database import init_db

app = FastAPI(
    title="Akıllı Tarif ve Buzdolabı Stok Takibi",
    description="Buzdolabı stoklarını takip eden ve tarif öneren uygulama API'si",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {
        "message": "Akıllı Tarif API'si çalışıyor!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

from fastapi import FastAPI
from src.infrastructure.database import init_db

app = FastAPI(
    title="Akıllı Tarif ve Buzdolabı Stok Takibi",
    description="Buzdolabı stok ve tarif yönetim sistemi",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


@app.get("/")
def home():
    return {
        "message": "Akıllı Tarif API'si çalışıyor!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }

from fastapi import FastAPI
from src.infrastructure.database import init_db
from src.api.item_routes import router as item_router

app = FastAPI(
    title="Akıllı Tarif ve Buzdolabı Stok Takibi",
    description="Buzdolabı stok ve tarif yönetim sistemi",
    version="1.0.0"
)


@app.on_event("startup")
def startup():
    init_db()


app.include_router(item_router)


@app.get("/")
def home():
    return {
        "message": "Akıllı Tarif API'si çalışıyor!",
        "status": "success"
    }


@app.get("/health")
def health_check():
    return {"status": "healthy"}

