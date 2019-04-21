from selenium.webdriver import Chrome
from selenium.common.exceptions import NoSuchElementException
import time
import random
from smsapi import Api
from juhe import image_vcode
from imageLook import crop_image_vcode
from config import *


def get_username(phone):
    return "".join([y[0] for y in [random.choices([chr(x) for x in range(97, 123)]) for i in range(5)]]) + str(phone)[:5]


# 创建 Api 对象
api = Api(username=sms_api_username, password=sms_api_password, productId=sms_api_product_id)
api.login()

while True:
    browser = Chrome()

    # 打开链接
    browser.get(share_link)

    time.sleep(2)
    # 点击免费听
    freeListen = browser.find_element_by_class_name("tsw-tobuy__isfree")
    freeListen.click()
    time.sleep(2)

    # 添加手机号
    phone_number = api.get_phone()

    smsLogin_send_phone = browser.find_element_by_id("smsLogin-username")

    if not phone_number:
        phone_number = api.get_phone()
    smsLogin_send_phone.send_keys(phone_number)
    time.sleep(2)

    # 点击发送验证码
    smsLogin_send_smsButton = browser.find_element_by_id("smsLogin-verifyCodeSend")
    smsLogin_send_smsButton.click()
    # 点击 快速注册
    time.sleep(3)
    try:
        browser.find_element_by_id("smsreg-ok-btn").click()
    except NoSuchElementException as e:
        api.add_to_blacklist(phone_number)
        print("[-] phone number is used, retry and reload browser...")
        browser.quit()
        continue

    time.sleep(2)

    # 手动输入验证码
    # sms_key = input("输入图形验证码: ")
    # 获取验证码图片
    # browser.get_screenshot_as_file("shot.png")
    # crop_image_vcode("shot.png", (544, 117), (115, 55))
    # # 验证码识别
    # vcode = image_vcode()
    #
    # browser.find_element_by_id("vcode-dialogVerifyCode").send_keys(vcode)
    # browser.find_element_by_id("vcode-submit").click()
    # time.sleep(2)

    while "smsLogin-password" not in browser.page_source:

        browser.find_element_by_id("vcode-dialogVerifyCode").clear()
        vcode_img = browser.find_element_by_id("verifyImgSrc")
        vcode_image_x = vcode_img.location.get("x")
        vcode_image_y = vcode_img.location.get("y")
        vcode_image_w = vcode_img.size.get("width")
        vcode_image_h = vcode_img.size.get("height")

        vcode_img.click()
        time.sleep(2)

        # 获取验证码图片
        browser.get_screenshot_as_file("shot.png")
        crop_image_vcode("shot.png", (vcode_image_x, vcode_image_y), (vcode_image_w, vcode_image_h))
        # 验证码识别
        vcode = image_vcode()

        browser.find_element_by_id("vcode-dialogVerifyCode").send_keys(vcode)
        browser.find_element_by_id("vcode-submit").click()
        time.sleep(2)

    # 输入 手机验证码
    sms_code = api.get_sms_by_phone(phone_number)

    if sms_code is None:
        print("[-] phone number is bad, quit browser and reload browser..")
        browser.quit()
        continue
    browser.find_element_by_id("smsLogin-password").send_keys(sms_code)
    time.sleep(2)
    browser.find_element_by_id("smsLogin-submit").click()
    time.sleep(2)

    # 输入用户名, 密码
    username = get_username(phone_number)
    password = "baidupan123"

    browser.find_element_by_id("setuname_pwd-username").send_keys(username)
    browser.find_element_by_id("setuname_pwd-password").send_keys(password)
    browser.find_element_by_id("setuname_pwd-submit").click()
    print("\t[+] Username: {}\t Password: {}\n".format(username, password))
    time.sleep(4)
    with open("user.log", 'a') as f:
        f.write("{},{}\n".format(username, password))

    # 点击免费听
    browser.find_element_by_class_name("tsw-tobuy__isfree").click()
    time.sleep(2)
    # 同意并继续
    browser.find_element_by_class_name("is-sure").click()
    time.sleep(2)
    browser.find_element_by_class_name("tsw-tobuy__isfree").click()
    time.sleep(3)

    browser.quit()
