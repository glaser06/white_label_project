import os.path
import sys
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from . import DataStore

from .mongo import UserStore, PostStore
from app.entities.schema import TemplateSchema, User, Template

import uuid

class TemplateService(object):
    def __init__(self, repo_client=DataStore(adapter=PostStore)):
        self.repo_client = repo_client

    def add_default_templates(self):
        if len(self.find_all_templates()) == 0 :
            default_template = {
                'name': 'default', 
                'main_css_url': 'local'
            }

    def default_template(self): 
        return self.find_template_by_name('default')

    def find_all_templates(self):
        templates  = self.repo_client.find_all({})
        print(templates)
        return [TemplateSchema().load(template).data for template in templates]

    def find_template(self, template_id):
        json = self.repo_client.find({'id': template_id})
        if json is None: 
            return None
        template = TemplateSchema().load(json).data
        return template

    def find_template_by_name(self, name):
        json = self.repo_client.find({'name': name})
        if json is None: 
            return None
        template = TemplateSchema().load(json).data
        return template

    def find_templates_for_user(self, user):

        json = self.repo_client.find({'id': user.template_id})
        print(json)
        if json is None: 
            return None
        templates = [TemplateSchema().load(template).data for template in json]
        print(templates)
        return templates



    def create_template(self, template_data):
        template = TemplateSchema().load(template_data).data
        print(template)
        template.id = uuid.uuid4()
        result = TemplateSchema().dump(template)

        self.repo_client.create(result.data)
        return result.data
