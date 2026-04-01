from sqlalchemy.orm import Mapped, relationship

from .base import Base

class City(Base):
    city:Mapped[str]

    organisations: Mapped[list["Organisations"]] = relationship(
        back_populates="city"
    )

    def __repr__(self):
        return self.city
