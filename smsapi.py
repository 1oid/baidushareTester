import requests
import time
import re

api_server = "http://api.duomi01.com/api"


class Api(object):

    def __init__(self, username, password, productId):
        self.username = username
        self.password = password
        self.token = ""
        self.product_id = productId

    def get_response(self, data):
        return data.strip().split("|")

    def login(self):
        r = requests.get(api_server + "?action=loginIn&name={}&password={}".format(self.username, self.password))

        status, token = self.get_response(r.text)

        if status == "1":
            self.token = token
            print("[+] get token {}".format(self.token))

    def get_phone(self):
        print("[+] request product Id: {}".format(self.product_id))
        r = requests.get(api_server + "?action=getPhone&sid={}&token={}".format(self.product_id, self.token))

        status, phone, *_ = self.get_response(r.text)

        if status == "1":
            print("[+] get phone number: {}".format(phone))
            return phone

    def get_sms_by_phone(self, phone):
        count = 0
        while count < 30:
            r = requests.get(api_server + "?action=getMessage&sid={}&token={}&phone={}".format(self.product_id, self.token, phone))

            status, sms_code, *_ = self.get_response(r.text)

            if status == "1":
                m = re.search(r'(\d{6})', sms_code)

                if m:
                    code = m.group(1)
                    print("[+] get sms code: {}".format(code))
                    return code
                return sms_code
            time.sleep(3)
            print("[-] sms code not recived, retry...")
            count += 1

        # 超过次数 加入到黑名单
        self.add_to_blacklist(phone)

    def add_to_blacklist(self, phone):
        r = requests.get(api_server + "?action=addBlacklist&sid={}&phone={}&token={}".format(self.product_id, phone, self.token))

        status, *_ = self.get_response(r.text)

        if status:
            print("[-] add to the backlist, phone: {}".format(phone))


