from flask import Flask,request,jsonify
import os
from idserver import FzuOpenID

app = Flask(__name__)

token = os.getenv("AppToken")

@app.route('/',methods=["POST"])
def idserver():
    content = request.json
    if not "token" in content or content["token"]!=token:
        return jsonify({"message":"Token验证错误"}),400
    if not "id" in content or not "pwd" in content:
        return jsonify({"message":"参数错误"}),400
    server = FzuOpenID()
    message="登陆成功"
    name,sno="",""
    try:
        name,sno=server.Login(content['id'],content['pwd'])
    except:
        message="登陆失败"
    return jsonify({"name":name,"sno":sno,"message":message})

if __name__ == "__main__":
    app.run("0.0.0.0",port="80",debug=False)