import json
from app.database.models import async_session
from app.database.models import  GoogleSheets, User
from sqlalchemy import select, desc
from sqlalchemy import update as sql_update



async def set_user(tg_id, email):
    async with async_session() as session:
        users_tg_id = await session.scalars(select(User))

        list_tg_id = []

        for i in users_tg_id.all():
            list_tg_id.append(i.tg_id)

        if tg_id not in list_tg_id:
            session.add(User(tg_id=tg_id, email=email))
            await session.commit()
        

# async def set_data(category, date, amount, user_tg_id):
#     async with async_session() as session:
#         await session.scalar(select(Data))
#         session.add(Data(category=category, date=date, amount=amount, user_tg_id=user_tg_id))
#         await session.commit()


async def set_data_google_sheets(name_table, id_google_sheets, user_tg_id, categories):
    async with async_session() as session:
        await session.scalar(select(GoogleSheets))
        session.add(GoogleSheets(name_table=name_table, id_google_sheets=id_google_sheets, user_tg_id=user_tg_id, categories=categories))
        await session.commit()


async def set_category(category, tg_id):
    async with async_session() as session:
        result = await session.scalar(select(GoogleSheets.categories).filter(GoogleSheets.user_tg_id == tg_id))
        # print(result)
        # result = list(result)
        result.append(category)
        print(result)
        print(type(result))
        stmt = sql_update(GoogleSheets).where(GoogleSheets.user_tg_id == tg_id).values(categories=json.dump(result))
        await session.execute(stmt)
        await session.commit()


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


async def get_user_email(tg_id):
    async with async_session() as session:
        user_email = await session.scalar(select(User.email).filter(User.tg_id == tg_id))
        return user_email

# async def get_data_google_sheets():
#     async with async_session() as session:
#         result = await session.execute(select(Data))

#         records = result.scalars()

#         return records
    

# async def delete_value_data(tg_id):
#     async with async_session() as session:
#         result = await session.execute(select(Data)
#         .filter(Data.user_tg_id == tg_id)
#         .order_by(desc(Data.id)))

#         obj = result.scalar()
        
#         await session.delete(obj)

#         await session.commit()


async def filter_name_google_sheets(tg_id):
    async with async_session() as session:
        query = select(GoogleSheets).filter(GoogleSheets.user_tg_id == tg_id)

        result = await session.execute(query)

        records = result.scalar()

        return records.name_table
    

async def filter_id_google_sheets(tg_id):
     async with async_session() as session:
        query = select(GoogleSheets).filter(GoogleSheets.user_tg_id == tg_id)

        result = await session.execute(query)

        records = result.scalar()

        return records.id_google_sheets
    

async def get_categories(tg_id):
    async with async_session() as session:
        query = select(GoogleSheets.categories).filter(GoogleSheets.user_tg_id == tg_id)

        result = await session.execute(query)

        records = result.scalars()

        all_category = []

        for i in records:
            for n in i:
                all_category.append(n)

        return all_category


async def delete_category(tg_id):
    pass
    # async with async_session() as session:
    #     result = await session.execute(select(Category)
    #     .filter(Category.user_tg_id == tg_id)
    #     .order_by(desc(Category.id)))

    #     obj = result.scalar()
        
    #     await session.delete(obj)

    #     await session.commit()
async def delete_user(tg_id):
    async with async_session() as session:
        async with async_session() as session:
            result = await session.execute(select(User)
            .filter(User.tg_id == tg_id)
            .order_by(desc(User.tg_id)))

            obj = result.scalar()
            
            await session.delete(obj)

            await session.commit()
