import requests
from base64 import b64encode
from db import BaiduShareDb
from config import *


def image_vcode():
    db = BaiduShareDb(db_server, db_user, db_pwd, db_select)
    APPKEY = db.fetch_appkey()
    CODETTPE = "1004"

    if not APPKEY:
        return input("[!!!]所有appkey的次数都用尽, 识别失败, 请手动输入验证码: ")

    target = "http://op.juhe.cn/vercode/index"

    with open("complated.png", 'rb') as f:
        image = f.read()

    data = {
        "key": APPKEY,
        "codeType": CODETTPE,
        "base64Str": b64encode(image),
        "dtype": "json"
    }

    r = requests.post(target, data=data)

    if r.json().get("error_code") == 0:
        vcode = r.json().get("result")
        print("[+] get screenshot vcode: {}".format(vcode))
        return r.json().get("result")
    elif r.json().get("error_code") == 10012:
        pass
    else:
        return input("识别失败, 请手动输入验证码: ")
