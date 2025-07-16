from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_session
from app.models.product import ProductCreate, ProductResponse
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])

@router.post("/product", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    session: AsyncSession = Depends(get_session)
):
    service = InventoryService(session)
    return await service.create_product(product)

@router.get("/product/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(get_session)
):
    service = InventoryService(session)
    product = await service.get_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
