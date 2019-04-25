import os.path
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from . import DataStore

from .firestore import UserStore, PostStore
from app.entities.schema import Post, PostSchema, User

import uuid

class PostService(object):
    def __init__(self, repo_client=DataStore(adapter=PostStore)):
        self.repo_client = repo_client




    def find_all_posts(self):
        posts  = self.repo_client.find_all({})
        if posts is None: 
            return []
        print(posts)
        return [PostSchema().load(post).data for post in posts]

    def find_post(self, post_id):
        json = self.repo_client.find({'id': post_id})
        if json is None: 
            return None
        post = PostSchema().load(json).data
        return post

    def find_posts_by_user(self, user):

        json = self.repo_client.find_all({'user_id': user.id})
        print(json)
        if json is None: 
            return []
        posts = [PostSchema().load(post).data for post in json]
        print(posts)
        return posts



    def create_post_for(self, user, post_data):
        post = PostSchema().load(post_data).data
        print(post)
        post.id = uuid.uuid4()
        post.user_id = user.id
        result = PostSchema().dump(post)

        self.repo_client.create(result.data)
        return user
