from google.cloud import firestore

class CloudStore(object):
    def __init__(self):
        self.client = firestore.Client()

    def find_all(self, selector):
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
        if big_query is None:
            big_query = self.db
        results = big_query.get()
        json = [user.to_dict() for user in results]
        if len(json) == 0:
            return None
        return json
    def find(self, selector):
        result = self.find_all(selector)
        if result is None: 
            return None
        return result[0]

class UserStore(CloudStore): 
    def __init__(self):
        super().__init__()
        self.db = self.client.collection('users')


    

    def create(self, user):
        # self.db.document(user['id']).set(user)
        return self.db.document(user['id']).set(user)


class PostStore(CloudStore): 
    def __init__(self):
        super().__init__()
        self.db = self.client.collection('posts')

    def create(self, post):
        return self.db.document(post['id']).set(post)

    # 
   


class TemplateStore(CloudStore): 

    def __init__(self):
        super().__init__()
        self.db = self.client.collection('templates')

    def create(self, template):
        return self.db.document(template['id']).set(template)



