from database.users_data import users
from schemas.user_schemas import*
from services.exceptions import UserNotFoundError,BadRequestError
from config.settings import settings

def set_up_groq():
    api_key = settings.groq_api_key
    model = settings.groq_model
    key_exist = False
    if api_key:
        key_exist = True

    return {
        "model" : model,
        "key_exist" : key_exist
    }



def create_user(data):
    new_id = max(users.keys())+1
    users[new_id] = {"name":data.name, "age": data.age}
    messaage = {
        "user_id" : new_id,
        "name" : data.name,
        "age" : data.age
    }
    return messaage

def send_user(user_id):
    if user_id not in users:
        raise UserNotFoundError
    return {
        "user_id" : user_id,
        "name" : users[user_id]["name"],
        "age" : users[user_id]["age"]
    }

def get_users(limit, offset, min_age):
    list_user_response = []
    for key,element in users.items():
        if min_age is not None: 
            if element["age"] >= min_age:
                list_user_response.append({
                "user_id" : key,
                "name" : element["name"],
                "age" : element["age"]
                })
        else:
            list_user_response.append({
                "user_id" : key,
                "name" : element["name"],
                "age" : element["age"]
            }) 
    
    return { 
            "items" : list_user_response[offset:offset+limit],
            "limit" : limit,
            "offset" : offset,
            "total" : len(list_user_response)
        }

def del_user(user_id, confirm):
    if not confirm:
        return
    if user_id not in users:
        raise UserNotFoundError
    
    del users[user_id]
    return

def update_user(user_id, update):
    if user_id not in users:
        raise UserNotFoundError
    
    users[user_id]["age"] = update.age
    users[user_id]["name"] = update.name
    return {
        "user_id" : user_id,
        "name" : users[user_id]["name"],
        "age" : users[user_id]["age"]
    }
    


def update_patch(user_id:int, patch:UpdatePatch):
    if user_id not in users:
            raise UserNotFoundError
    
    if patch.name is None and patch.age is None:
        raise BadRequestError

    
    elif patch.name is None:
        users[user_id]["age"] = patch.age

    elif patch.age is None:
        users[user_id]["name"] = patch.name

    else:
        users[user_id]["name"] = patch.name
        users[user_id]["age"] = patch.age
    return {
        "user_id" : user_id,
        "name" : users[user_id]["name"],
        "age" : users[user_id]["age"]
    }

