from flask import Flask,jsonify,request
from flask_restful import Api,Resource
from pymongo import MongoClient

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.aNewDB
UserNum = db["UserNum"]

UserNum.insert_one({
    'num_of_users': 0
})

class Visit(Resource):
    def get(self):
        prev_num = UserNum.find({})[0]["num_of_users"]
        new_num = prev_num + 1
        UserNum.update_one({},{"$set":{"num_of_users":new_num}})
        resp = {
            "Message": f"You are the user no : {new_num}",
            "Status Code": 200
        }
        return resp


def checkData(postedData,functionName):
    if functionName in ["add","substract","multiply","devide"]:
        if "x" not in postedData or "y" not in postedData:
            return 301
        elif functionName == "devide" and postedData["y"] == 0:
            return 302
        else:
            return 200
        
        

def returnData(postedData,functionName,status_code):
    res = 0
    if "x" in postedData and "y" in postedData:
        if functionName == "add":
            res = postedData["x"] + postedData["y"]
        elif functionName == "substract":
            res = postedData["x"] - postedData["y"]
        elif functionName == "multiply":
            res = postedData["x"] * postedData["y"]
        elif functionName == "devide":
            if postedData["y"] == 0:
                return False
            res = postedData["x"] / postedData["y"]
        resp = {
            "Sum": res,
            "Status Code": status_code
        }
        return resp
    else:
        return False



class Add(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkData(postedData,"add")

        if status_code != 200:
            resp = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(resp)

        resp = returnData(postedData,"add",status_code)

        return jsonify(resp)
    
class Substract(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkData(postedData,"substract")

        if status_code != 200:
            resp = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(resp)

        resp = returnData(postedData,"substract",status_code)

        return jsonify(resp)
    
class Multiply(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkData(postedData,"multiply")

        if status_code != 200:
            resp = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(resp)

        resp = returnData(postedData,"multiply",status_code)

        return jsonify(resp)
    
class Devide(Resource):
    def post(self):
        postedData = request.get_json()

        status_code = checkData(postedData,"devide")

        if status_code != 200:
            resp = {
                "Message": "An error occured",
                "Status Code": status_code
            }
            return jsonify(resp)

        resp = returnData(postedData,"devide",status_code)

        return jsonify(resp)   



api.add_resource(Add,"/add")
api.add_resource(Substract,"/substract")
api.add_resource(Multiply,"/multiply")
api.add_resource(Devide,"/devide")
api.add_resource(Visit,"/visit")


@app.route("/")
def hello_world():
    response = {
        "yassine" : "laamiri"
    }
    return jsonify(response)


@app.route("/sum",methods=["POST"])
def sum_nums():
    req = request.get_json()
    x = req["x"]
    y = req["y"]
    res = {"results" : x+y}
    return jsonify(res),200


if __name__ == "__main__":
    app.run(host="0.0.0.0",port=80,debug=True)