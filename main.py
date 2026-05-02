from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.models  # noqa: F401 — registers all ORM models with Base.metadata
from app.core.config import settings
from app.core.database import Base, engine
from app.routers import category, payment_method, product, region, sales_order


@asynccontextmanager
async def lifespan(application: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


application = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    debug=settings.DEBUG,
    lifespan=lifespan,
    redirect_slashes=False,
)

application.include_router(category.router, prefix="/categories", tags=["Categories"])
application.include_router(region.router, prefix="/regions", tags=["Regions"])
application.include_router(payment_method.router, prefix="/payment-methods", tags=["Payment Methods"])
application.include_router(product.router, prefix="/products", tags=["Products"])
application.include_router(sales_order.router, prefix="/sales-orders", tags=["Sales Orders"])


@application.get("/health", tags=["Health"])
def health():
    return {"status": "ok", "app": settings.APP_NAME}
