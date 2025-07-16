from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.product import ProductCreate, ProductResponse
from app.db.database import Base
from sqlalchemy import Column, Integer, String, Float

class Product(Base):
    _tablename_ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)

class InventoryService:
    def _init_(self, session: AsyncSession):
        self.session = session

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        db_product = Product(**product.dict())
        self.session.add(db_product)
        await self.session.commit()
        await self.session.refresh(db_product)
        return ProductResponse.from_orm(db_product)

    async def get_product(self, product_id: int) -> ProductResponse:
        result = await self.session.execute(select(Product).where(Product.id == product_id))
        product = result.scalars().first()
        if product:
            return ProductResponse.from_orm(product)
        return None