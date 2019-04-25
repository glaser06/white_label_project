from google.cloud import firestore

class CloudStore(object):
    def __init__(self):
        self.client = firestore.Client()

class UserStore(CloudStore): 
    def __init__(self):
        super().__init__()
        self.db = self.client.collection('users')


    def find_all(self, selector):
        return self.db.get()

    def find(self, selector):
        queries = [] 
        for key in selector:
            queries.append([key, '==', selector[key]])
        print(*queries)
        big_query = None
        for query in queries:
            print(*query)
            if big_query is None :
                big_query = self.db.where(*query)
            big_query = big_query.where(*query)

        return big_query.get()

    def create(self, user):
        # self.db.document(user['id']).set(user)
        return self.db.document(user['id']).set(user)


class PostStore(CloudStore): 

    def find_all(self, selector):
        return self.db.posts.find(selector)

    def create(self, post):
        return self.db.posts.insert_one(post)

    def find(self, selector):
        return self.db.posts.find_one(selector)


class TemplateStore(CloudStore): 

    def find_all(self, selector):
        return self.db.templates.find(selector)

    def create(self, post):
        return self.db.templates.insert_one(post)

    def find(self, selector):
        return self.db.templates.find_one(selector)

