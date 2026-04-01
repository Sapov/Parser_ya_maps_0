from sqlalchemy.orm import Mapped, relationship

from .base import Base

class Category(Base):
    category: Mapped[str]

    organisations: Mapped[list["Organisations"]] = relationship(
        back_populates="category"
    )

    def __repr__(self):
        return self.category