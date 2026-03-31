from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from parser.models import Base
from parser.models.organisations import Organisations
from parser.models.city import City
from parser.models.category import Category
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)


class DB:
    def __init__(self):
        self.engine = create_engine(
            "sqlite:////home/sasha/PycharmProjects/ParingYaMaps/parsers/core/db.sqlite3",
            echo=False,
        )
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        Base.metadata.create_all(self.engine)

    def add_items_link(self, items_link: dict) -> None:
        session = self.Session()
        try:
            category_name = items_link.get("category")
            category = (
                session.query(Category).filter_by(name_category=category_name).first()
            )
            if not category:
                category = Category(name_category=category_name)
            session.add(category)

            city_name = items_link.get("city")
            city = session.query(City).filter_by(city=city_name).first()
            if not city:
                city = City(city=city_name)
                session.add(city)

            item = Organisations(
                link=items_link.get("link"),
                title=items_link.get("title"),
                rating_yandex=items_link.get("rating_yandex"),
                estimation=items_link.get("estimation"),
                category=category,
                city=city,
            )
            session.add(item)
            session.commit()
            # Печатаем ДО коммита или используем expire_on_commit=False
            logger.info(f"Добавлен элемент с ID: {item.id}")
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")
            raise  # Переподнимаем исключение для диагностики
        finally:
            session.close()

    def get_all_links(self) -> list[Organisations]:
        """Получить все записи из таблицы"""
        session = self.Session()
        try:
            stmt = select(Organisations)
            result = session.execute(stmt)
            return list(result.scalars())
        finally:
            session.close()

    def get_links_filtered(self, min_rating: float = 4.0) -> list[Organisations]:
        """Получить записи с рейтингом выше указанного"""
        session = self.Session()
        try:
            stmt = select(Organisations).where(
                Organisations.rating_yandex >= str(min_rating)
            )
            return list(session.scalars(stmt))
        finally:
            session.close()

    def get_link_by_id(self, link_id: int) -> Organisations | None:
        """Получить одну запись по ID"""
        session = self.Session()
        try:
            return session.get(Organisations, link_id)
        finally:
            session.close()

    def get_links_paginated(
        self, page: int = 1, per_page: int = 10
    ) -> list[Organisations]:
        """Постраничное чтение"""
        session = self.Session()
        try:
            stmt = select(Organisations).limit(per_page).offset((page - 1) * per_page)
            return list(session.scalars(stmt))
        finally:
            session.close()

    def get_links_paginated_up(
        self, page: int = 1, per_page: int = 10
    ) -> list[Organisations]:
        """Постраничное чтение"""
        session = self.Session()
        try:
            stmt = select(Organisations).limit(per_page).offset((page - 1) * per_page)
            lst = []
            for i in list(session.scalars(stmt)):
                lst.append(
                    {
                        "id": i.id,
                        "link": i.link,
                        "title": i.title,
                        "rating_yandex": i.rating_yandex,
                        "estimation": i.estimation,
                        "phone": i.phone,
                        "address": i.address,
                        "site": i.site,
                        "category": i.category,  # "mail":i.mail,
                    }
                )
            return lst
        finally:
            session.close()

    def add_items_organisations(self, items_link: dict) -> None:
        # добавляем организации с сайтом и тел
        session = self.Session()
        try:
            item = Organisations(
                link=items_link.get("link"),
                title=items_link.get("title"),
                rating_yandex=items_link.get("rating_yandex"),
                estimation=items_link.get("estimation"),
                phone=items_link.get("phone"),
                address=items_link.get("address"),
                site=items_link.get("site"),
                category=items_link.get("category"),
                city=items_link.get("city"),
            )
            session.add(item)
            session.commit()
            # Печатаем ДО коммита или используем expire_on_commit=False
            logger.info(f"Добавлена организация с ID: {item.id}")
        except Exception as e:
            session.rollback()
            print(f"Ошибка: {e}")
            raise  # Переподнимаем исключение для диагностики
        finally:
            session.close()

    def get_all_sites(self) -> list[Organisations]:
        """Получить все записи из таблицы"""
        session = self.Session()
        try:
            stmt = select(Organisations)
            result = session.execute(stmt)
            lst = []
            for i in list(result.scalars()):
                lst.append(
                    {
                        "id": i.id,
                        "link": i.link,
                        "title": i.title,
                        "rating_yandex": i.rating_yandex,
                        "estimation": i.estimation,
                        "phone": i.phone,
                        "address": i.address,
                        "site": i.site,
                        # "category": i.category,  # "mail":i.mail,
                    }
                )
            return lst

        finally:
            session.close()

    def update_record(self, items_link: dict):
        """
        обновляем запись добавляя тел, адрес, сайт
        """
        with Session(self.engine) as session:
            entry = session.query(Organisations).get(items_link.get("id"))
            if entry:
                entry.phone = items_link.get("phone")
                entry.address = items_link.get("address")
                entry.site = items_link.get("site")

                logger.info(f"Обновлена организация с ID: {entry.id}")
            session.commit()


# Проверка работы
if __name__ == "__main__":
    db = DB()
    print(db.get_all_sites())