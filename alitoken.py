#!/usr/local/bin/python3

import time
import pyqrcode
import requests

if __name__ == '__main__':
    data = requests.post('http://api.extscreen.com/aliyundrive/qrcode', data={
        'scopes': ','.join(["user:base", "file:all:read", "file:all:write"]),
        "width": 500,
        "height": 500,
    }).json()['data']
    qr_link = data['qrCodeUrl']
    sid = data['sid']
    # 两种登录方式都可以
    # web登录, 打开链接登录
    #print(f'https://www.aliyundrive.com/o/oauth/authorize?sid={sid}')
    qr_link = "https://www.aliyundrive.com/o/oauth/authorize?sid=" + sid
    qr = pyqrcode.create(qr_link, error="L")
    print(qr.terminal(quiet_zone=1))
 
    while True:
        time.sleep(3)
        status_data = requests.get(f'https://openapi.alipan.com/oauth/qrcode/{sid}/status').json()
        status = status_data['status']
        if status == 'LoginSuccess':
            auth_code = status_data['authCode']
            break
    # 使用code换refresh_token
    token_data = requests.post('http://api.extscreen.com/aliyundrive/token', data={
        'code': auth_code,
    }).json()['data']
    refresh_token = token_data['refresh_token']
    file = open("/data/myopentoken.txt", "w")
    file.write(refresh_token)
    file.close()
    file = open("/data/open_tv_token_url.txt", "w")
    file.write("https://alitv.sakurapy.de/token")
    file.close()


