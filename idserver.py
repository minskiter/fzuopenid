#!/usr/bin/python
# -*- coding: UTF-8 -*-
import dukpy
import io
import requests
import re
from PIL import Image
import pytesseract
from io import BytesIO

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Mobile Safari/537.36 Edg/86.0.622.43',
    'Accept-Encoding': 'gzip, deflate',
    'Accept': '*/*',
    'Connection': 'keep-alive'
}


class FzuOpenID():
    def __init__(self):
        f = open("encrypt.js")
        self.__encrypt = f.read()
        f.close()
        self.s = requests.Session()

    def Login(self, id, pwd):
        pwdDefaultEncryptSalt = None
        r = self.s.get("http://id.fzu.edu.cn/authserver/login",
                       headers=headers)
        pwdDefaultEncryptSalt = re.search(
            r'pwdDefaultEncryptSalt = "(.*)"', r.text).group(1)
        lt = re.search(r'lt" value="(.*)"', r.text).group(1)
        execution = re.search(r'"execution" value="(.*)"', r.text).group(1)
        hasCode = self.s.get("http://id.fzu.edu.cn/authserver/needCaptcha.html?username={0}&pwdEncrypt2=pwdEncryptSalt".format(id)).text
        if hasCode=="false":
            hasCode=False
        else:
            hasCode=True
        code = ""
        if hasCode:
            code = self.getCaptcha()
        data = {
            'username': "{0}".format(id),
            'dllt': 'userNamePasswordLogin',
            'captchaResponse': code ,
            'password': dukpy.evaljs(self.__encrypt+"\nencryptAES('{0}','{1}')".format(pwd, pwdDefaultEncryptSalt)),
            'lt': lt,
            'execution': execution,
            "_eventId": "submit",
            'rmShown': "1"
        }
        headers['Content-Type']="application/x-www-form-urlencoded"
        r = self.s.post("http://id.fzu.edu.cn/authserver/login",headers=headers,data=data)
        name = re.search(r'data-name="name">(.*)',r.text).group(1).replace('\r','')
        sno = re.search(r'data-name="id">(.*)',r.text).group(1).replace('\r','')
        return name,sno

    def getCaptcha(self):
        r = self.s.get("http://id.fzu.edu.cn/authserver/captcha.html")
        if r.status_code == 200:
            img = Image.open(io.BytesIO(r.content))
            img = img.convert("L")
            pixels = img.load()
            for x in range(img.width):
                for y in range(img.height):
                    if pixels[x, y] > 127.5:
                        pixels[x, y] = 255
                    else:
                        pixels[x, y] = 0
            textCode = pytesseract.image_to_string(img,lang="eng")
            textCode = re.sub("\W", "", textCode)
            return textCode
        return ""

if __name__ == "__main__":
    openid = FzuOpenID()
    try:
        name,sno = openid.Login("name", "sno")
        print(name)
        print(sno)
    except:
        print("密码错误")
