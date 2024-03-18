from sqlalchemy import update, select, delete, text
from src.db.abstract_repository import AbstractRepository
from src.db.dependencies import get_db_session
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import load_only
from src.db.models import models
from starlette.requests import Request


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, request: Request):
        self.request = request

    async def edit_many(
        self,
        ids: list,
        data,
    ):
        async for session in get_db_session(self.request):
            stmt = update(self.model).where(self.model.id.in_(ids)).values(**data)
            await session.execute(stmt)

    async def find_one(self, filter_by: dict, order_by=None, fields=None):
        async for session in get_db_session(self.request):
            query = select(self.model).filter_by(**filter_by)

            if order_by:
                query = query.order_by(order_by)

            if fields:
                field_attributes = [getattr(self.model, field) for field in fields]
                query = query.options(load_only(*field_attributes))
            res = await session.execute(query)
            result = res.scalars().first()

        return result

    async def find_all(
        self, filter_by: dict, order_by=None, offset=0, limit=None, fields=None
    ):
        async for session in get_db_session(self.request):
            query = select(self.model).filter_by(**filter_by)

            if order_by == "id":
                query = query.order_by(self.model.id)

            if offset or limit:
                query = query.offset(offset).limit(limit)

            if fields:
                # Преобразуем имена полей в соответствующие атрибуты модели
                field_attributes = [getattr(self.model, field) for field in fields]
                # Используем атрибуты модели в методе load_only
                query = query.options(load_only(*field_attributes))

            res = await session.execute(query)
            results = res.scalars().all()

            return results

    async def edit_one(self, id_: int, data):
        async for session in get_db_session(self.request):
            stmt = (
                update(self.model)
                .where(self.model.id == id_)
                .values(**data)
                .returning(self.model)
            )
            res = await session.execute(stmt)
            results = res.scalars().first()

            return results

    async def insert_one(self, data):
        async for session in get_db_session(self.request):
            stmt = insert(self.model).returning(self.model).on_conflict_do_nothing()
            result = await session.execute(stmt, data)
            return result.scalars().first()

    async def insert_many(self, data):
        async for session in get_db_session(self.request):
            ids = await session.execute(
                insert(self.model).on_conflict_do_nothing().returning(self.model), data
            )
            return ids.scalars().all()

    async def execute_query(self, query: str):
        async for session in get_db_session(self.request):
            sql = text(query)
            await session.execute(sql)

    async def delete_one(self, id_: int):
        async for session in get_db_session(self.request):
            stmt = delete(self.model).where(self.model.id == id_)
            result = await session.execute(stmt)
            if result.rowcount > 0:
                return {"message": "Deleted successfully."}
            else:
                return None


class ContactsRepository(SQLAlchemyRepository):
    model = models.Contact
