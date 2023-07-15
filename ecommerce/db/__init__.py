from ecommerce.schemas.user import UserInDB

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "",
        "disabled": False,
    }
}

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

# async def get_user(db, username:str):
#     if username in db:
#         user_dict = db[username]
#         return UserInDB(**user_dict)

