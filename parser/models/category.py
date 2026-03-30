from sqlalchemy.orm import Mapped

from .base import Base

class Category(Base):
    category: Mapped[str]

