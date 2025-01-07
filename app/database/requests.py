from app.database.models import async_session
from app.database.models import Data, GoogleSheets, User
from sqlalchemy import select, desc




async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalars(select(User))
        if user.first() == None:
            session.add(User(tg_id=tg_id))
            await session.commit()
        # else:
        #     user = await session.scalars(select(User))
        #     for i in user:
        #         if tg_id != i:
        #             session.add(User(tg_id=tg_id))
        #             await session.commit()

        #             print(tg_id)
        #             break


async def set_data(category, date, amount, user_tg_id):
    async with async_session() as session:
        await session.scalar(select(Data))
        session.add(Data(category=category, date=date, amount=amount, user_tg_id=user_tg_id))
        await session.commit()


async def set_data_google_sheets(name_table, id_google_sheets, user_tg_id):
    async with async_session() as session:
        await session.scalar(select(GoogleSheets))
        session.add(GoogleSheets(name_table=name_table, id_google_sheets=id_google_sheets, user_tg_id=user_tg_id))
        await session.commit()


async def get_info_google_sheets():
    async with async_session() as session:
        query = select(GoogleSheets)

        result = await session.execute(query)
        
        records = result.scalar()

        return records


async def get_user_tg_id():
    async with async_session() as session:
        query = select(User)

        result = await session.execute(query)

        records = result.scalar()

        return records


async def get_data_google_sheets():
    async with async_session() as session:
        result = await session.execute(select(Data))

        records = result.scalars()

        return records
    

async def delete_value():
    async with async_session() as session:
        result = await session.execute(select(Data).order_by(desc(Data.id)))

        obj = result.scalar()
        
        await session.delete(obj)

        await session.commit()