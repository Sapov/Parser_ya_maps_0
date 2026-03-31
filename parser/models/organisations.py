from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from base import Base

class Organisations(Base):
    __tablename__ = "organisations"  # Fixed typo in table name
    link: Mapped[str | None]
    title: Mapped[str | None]
    rating_yandex: Mapped[str | None]
    estimation: Mapped[str | None]
    phone: Mapped[str | None]
    address: Mapped[str | None]
    site: Mapped[str | None]

    # Foreign key and relationship with Category
    category_id: Mapped[int] = mapped_column(ForeignKey("category.id"))
    category: Mapped["Category"] = relationship(
        back_populates="organisations", foreign_keys=[category_id]
    )

    # Foreign key and relationship with City
    city_id: Mapped[int] = mapped_column(ForeignKey("city.id"))
    city: Mapped["City"] = relationship(
        back_populates="organisations", foreign_keys=[city_id]
    )

    mail: Mapped[str | None]
    whatsapp: Mapped[str | None]
    telegram: Mapped[str | None]

    def __str__(self):
        return f"LINKS #{self.id} : Organisation: {self.title}"

    def __repr__(self):
        return str(self)