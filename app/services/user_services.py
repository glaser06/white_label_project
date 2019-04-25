# import sys
# sys.path.append('../')
import os.path
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from . import DataStore

# from .mongo import UserStore
from .firestore import UserStore
from .template_service import TemplateService

from app.entities.schema import UserSchema, User
import uuid

class UserService(object):
    def __init__(self, repo_client=DataStore(adapter=UserStore)):
        self.repo_client = repo_client


    def find_all_users(self):
        users  = self.repo_client.find_all({})
        return [UserSchema().load(user.to_dict()).data for user in users]

    def find_user(self, user_id):
        json = self.repo_client.find({'id': user_id})
        if json is None: 
            return None
        user = UserSchema().load([user.to_dict() for user in json][0]).data
        return user

    def find_user_by_name(self, username):
        json = self.repo_client.find({'username': username})
        # print([user.to_dict() for user in json][0])
        if json is None: 
            return None
        user = UserSchema().load([user.to_dict() for user in json][0]).data
        return user


    def create_user_for(self, user_data, password):
        user = UserSchema().load(user_data).data
        # user.template_id = TemplateService().default_template().id
        user.id = uuid.uuid4()
        user.set_password(password)
        result = UserSchema().dump(user)

        self.repo_client.create(result.data)
        return user

