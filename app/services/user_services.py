# import sys
# sys.path.append('../')
import os.path
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from . import DataStore

from .mongo import UserStore
from app.entities.schema import UserSchema, User
import uuid

class UserService(object):
  def __init__(self, repo_client=DataStore(adapter=UserStore)):
    self.repo_client = repo_client


    

  def find_all_users(self):
    users  = self.repo_client.find_all({})
    return [UserSchema().load(user).data for user in users]

  def find_user(self, user_id):
    json = self.repo_client.find({'id': user_id})
    if json is None: 
      return None
    user = UserSchema().load(json).data
    return user
  def find_user_by_name(self, username):
    json = self.repo_client.find({'username': username})
    if json is None: 
      return None
    user = UserSchema().load(json).data
    return user


  def create_user_for(self, user_data, password):
    user = UserSchema().load(user_data).data

    user.id = uuid.uuid4()
    user.set_password(password)
    result = UserSchema().dump(user)

    self.repo_client.create(result.data)
    return user

  #  def update_kudo_with(self, repo_id, githubRepo):
  #    records_affected = self.repo_client.update({'user_id': self.user_id, 'repo_id': repo_id}, self.prepare_kudo(githubRepo))
  #    return records_affected > 0

  #  def delete_kudo_for(self, repo_id):
  #    records_affected = self.repo_client.delete({'user_id': self.user_id, 'repo_id': repo_id})
  #    return records_affected > 0

  def dump(self, data):
    return UserSchema(exclude=['_id']).dump(data).data

  def prepare_kudo(self, githubRepo):
    data = githubRepo.data
    data['user_id'] = self.user_id
    return data