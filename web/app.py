from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.SentencesDatabase
users = db["Users"]


class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        hashed = bcrypt.hashpw(password.encode("utf8"),bcrypt.gensalt())

        users.insert_one({
            "Username": username,
            "Password": hashed,
            "Sentence": "",
            "Token": 6
        })

        resp = {
            "Message": "You have been registered",
            "Status Code": 200
        }

        return jsonify(resp)
    
def verify_pass(usrename,password):
    hashed_pass = users.find({
        "Username": usrename,
    })[0]["Password"]
    return bcrypt.hashpw(password.encode("utf8"),hashed_pass) == hashed_pass


def countTokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Token"]
    return tokens


class Store(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        sentence = postedData["sentence"]

        verify = verify_pass(username,password)

        if not verify:
            resp = {
                "Status Code": 302
            }
            return jsonify(resp)
        
        num_token = countTokens(username)

        if num_token <= 0:
            resp = {
                "Status Code": 301
            }
            return jsonify(resp)
        
        users.update_one({"Username": username},{"$set":{"Sentence":sentence,"Token":num_token-1}})

        resp = {
                "Message": "Sentence saved successfuly",
                "Status Code": 200
            }
        
        return jsonify(resp)


def getSentence(usermane):
    sentence = users.find({
        "Username": usermane
    })[0]["Sentence"]
    return sentence

class Retreive(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]


        verify = verify_pass(username,password)

        if not verify:
            resp = {
                "Status Code": 302
            }
            return jsonify(resp)
        
        sentence = getSentence(username)

        resp = {
            "Your Sentence": sentence
        }

        return jsonify(sentence)
        


api.add_resource(Register,"/register")
api.add_resource(Store,"/store")
api.add_resource(Retreive,"/retreive")


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)