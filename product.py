from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


@dataclass
class Product:
    name: str
    brand: str
    price: str
    currency: str
    shipping_suppliers: str
    url: str


class Base(DeclarativeBase):
    pass


class ProductORM(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100))
    brand: Mapped[str] = mapped_column(String(20))
    price: Mapped[Decimal] = mapped_column(Numeric(10, 4))
    currency: Mapped[str] = mapped_column(String(4))
    shipping_suppliers: Mapped[str] = mapped_column(String(100))
    url: Mapped[str] = mapped_column(String(100))

    @classmethod
    def from_dataclass(cls, data: Product) -> "ProductORM":
        return cls(
            name=data.name,
            brand=data.brand,
            price=data.price,
            currency=data.currency,
            shipping_suppliers=data.shipping_suppliers,
            url=data.url,
        )

    def to_dataclass(self) -> Product:
        return Product(
            name=self.name,
            brand=self.brand,
            price=str(self.price),
            currency=self.currency,
            shipping_suppliers=self.shipping_suppliers,
            url=self.url,
        )
