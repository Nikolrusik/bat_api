from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import selectinload, aliased
from sqlalchemy import select, delete


class BaseService:
    '''
    Base repository class for database operations
    '''
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_objects_list(self):
        '''
        Retrieve a list of all objects of the specified model.
        '''
        query = select(self.model).where()
        # async with self.session() as session:
        executed_items = await self.session.execute(query)
        result = executed_items.scalars().all()
        return result

    async def get_object_by_id(self, id: int):
        '''
        Retrieve an object by its ID.
        '''
        query = select(self.model).where(self.model.id == id)
        executed_items = await self.session.execute(query)
        result = executed_items.scalar_one_or_none()
        return result

    async def create_object(self, new_object: model):
        '''
        Create a new object
        '''
        try:
            async with self.session.begin():
                object = self.model(**new_object.dict())
                self.session.add(object)
                await self.session.commit()
            return object
        except Exception:
            pass

    async def update_object_by_id(self, updated_data: model, object_id: int):
        '''
        Update an existing object by its ID.
        '''
        try:
            stmt = select(self.model).filter(self.model.id == object_id)
            result = await self.session.execute(stmt)
            stored_item = result.scalar_one_or_none()

            if not stored_item:
                return None

            update_data = updated_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(stored_item, field, value)

            await self.session.commit()
            await self.session.refresh(stored_item)
            return stored_item
        except Exception:
            pass
