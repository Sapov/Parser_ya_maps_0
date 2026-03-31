from sqlalchemy.orm import Mapped

from .base import Base

class City(Base):
    city:Mapped[str]

    def __repr__(self):
        return self.city
