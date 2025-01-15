from app.database.models import async_session
from app.database.models import Data, GoogleSheets, User, Category
from sqlalchemy import select, desc




async def set_user(tg_id):
    async with async_session() as session:
        users_tg_id = await session.scalars(select(User))

        list_tg_id= []

        for i in users_tg_id.all():
            list_tg_id.append(i.tg_id)

        if tg_id not in list_tg_id:
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


async def set_category(category, user_tg_id):
    async with async_session() as session:
        await session.scalar(select(Category))
        session.add(Category(category=category, user_tg_id=user_tg_id))
        await session.commit()


async def get_categories(tg_id):
    async with async_session() as session:
        query = select(Category).filter(Category.user_tg_id == tg_id)

        result = await session.execute(query)

        records = result.scalars().all()

        all_category = []

        for i in records:
            all_category.append(i.category)

        return all_category


async def get_info_google_sheets():
    async with async_session() as session:
        result = await session.execute(select(GoogleSheets))

        records = result.scalar()

        return records


async def get_tg_id_from_google_sheets():
    async with async_session() as session:
        tg_id = await session.scalars(select(GoogleSheets))

        list_tg_id= []

        for i in tg_id.all():
            list_tg_id.append(i.user_tg_id)

        return list_tg_id


async def get_user_tg_id():
    async with async_session() as session:
        tg_id = await session.scalars(select(User))

        list_tg_id= []

        for i in tg_id.all():
            list_tg_id.append(i.tg_id)

        return list_tg_id


async def get_data_google_sheets():
    async with async_session() as session:
        result = await session.execute(select(Data))

        records = result.scalars()

        return records
    

async def delete_value_data(tg_id):
    async with async_session() as session:
        result = await session.execute(select(Data)
        .filter(Data.user_tg_id == tg_id)
        .order_by(desc(Data.id)))

        obj = result.scalar()
        
        await session.delete(obj)

        await session.commit()


async def delete_category(tg_id):
    async with async_session() as session:
        result = await session.execute(select(Category)
        .filter(Category.user_tg_id == tg_id)
        .order_by(desc(Category.id)))

        obj = result.scalar()
        
        await session.delete(obj)

        await session.commit()


async def filter_name_google_sheets(tg_id):
    async with async_session() as session:
        query = select(GoogleSheets).filter(GoogleSheets.user_tg_id == tg_id)
        # result = await session.execute(select(Data))

        result = await session.execute(query)

        records = result.scalar()

        return records.name_table
    
async def filter_id_google_sheets(tg_id):
     async with async_session() as session:
        query = select(GoogleSheets).filter(GoogleSheets.user_tg_id == tg_id)
        # result = await session.execute(select(Data))

        result = await session.execute(query)

        records = result.scalar()

        return records.id_google_sheets
    