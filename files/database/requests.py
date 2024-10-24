from files.database.models import async_session
from files.database.models import User
from sqlalchemy import select


async def set_user(user_id, name):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))

        if not user:
            session.add(User(user_id=user_id, username=name))
            await session.commit()


async def all_ids():
    async with async_session() as session:
        all_ids = await session.scalars(select(User.user_id))
        return all_ids


async def count_ids():
    async with async_session() as session:
        count_ids = await session.scalars(select(User.id))

        n = 0
        for e in count_ids:
            n += 1

        return n



