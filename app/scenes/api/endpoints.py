import sys
sys.path.append('../')
# import os.path
# import sys
# import time

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from flask import Flask, json, g, request
from app.services.datastore_service import Service as Kudo
from app.entities.schema import GithubRepoSchema
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/kudos", methods=["GET"])
def index():
 return json_response(Kudo("a").find_all_kudos())


@app.route("/kudos", methods=["POST"])
def create():
   github_repo = GithubRepoSchema().load(json.loads(request.data))
  
   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo = Kudo(g.user).create_kudo_for(github_repo)
   return json_response(kudo)


@app.route("/kudo/<int:repo_id>", methods=["GET"])
def show(repo_id):
 kudo = Kudo(g.user).find_kudo(repo_id)

 if kudo:
   return json_response(kudo)
 else:
   return json_response({'error': 'kudo not found'}, 404)


@app.route("/kudo/<int:repo_id>", methods=["PUT"])
def update(repo_id):
   github_repo = GithubRepoSchema().load(json.loads(request.data))
  
   if github_repo.errors:
     return json_response({'error': github_repo.errors}, 422)

   kudo_service = Kudo(g.user)
   if kudo_service.update_kudo_with(repo_id, github_repo):
     return json_response(github_repo.data)
   else:
     return json_response({'error': 'kudo not found'}, 404)

  
@app.route("/kudo/<int:repo_id>", methods=["DELETE"])
def delete(repo_id):
 kudo_service = Kudo(g.user)
 if kudo_service.delete_kudo_for(repo_id):
   return json_response({})
 else:
   return json_response({'error': 'kudo not found'}, 404)


def json_response(payload, status=200):
 return (json.dumps(payload), status, {'content-type': 'application/json'})

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')