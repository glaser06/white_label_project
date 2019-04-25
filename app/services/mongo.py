import os
from pymongo import MongoClient

COLLECTION_NAME = 'posts'

class MongoStore(object): 
  def __init__(self):
    mongo_url = os.environ.get('MONGO_URL')
    self.db = MongoClient(mongo_url).simple_posts



class UserStore(MongoStore): 

  def find_all(self, selector):
    return self.db.users.find({})

  def find(self, selector):
    return self.db.users.find_one(selector)

  def create(self, user):
   return self.db.users.insert_one(user)
  

class PostStore(MongoStore): 

  def find_all(self, selector):
    return self.db.posts.find(selector)

  def create(self, post):
   return self.db.posts.insert_one(post)

  def find(self, selector):
   return self.db.posts.find_one(selector)


class TemplateStore(MongoStore): 

  def find_all(self, selector):
    return self.db.templates.find(selector)

  def create(self, post):
   return self.db.templates.insert_one(post)

  def find(self, selector):
   return self.db.templates.find_one(selector)

