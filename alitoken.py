#!/usr/local/bin/python3

import time
import pyqrcode
import requests
import base64
import json
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def decrypt_AES256_CBC_PKCS7(ciphertext, key, iv):
    key = key[:32]
    key = key.ljust(32, "\0")
    decoded_ciphertext = base64.b64decode(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key.encode('utf8'), AES.MODE_CBC, iv=iv)
    decrypted_data = cipher.decrypt(decoded_ciphertext)
    unpadded_data = unpad(decrypted_data, AES.block_size)
    return unpadded_data.decode('utf8')

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
    token = requests.post('http://api.extscreen.com/aliyundrive//v2/token', data={
        'code': auth_code,
    }).json()
    token_data = token['data']
    ciphertext = token_data['ciphertext']
    iv = token_data['iv']
    key = "^(i/x>>5(ebyhumz*i1wkpk^orIs^Na."
    token_data = decrypt_AES256_CBC_PKCS7(ciphertext, key, iv)
    parsed_json = json.loads(token_data)
    refresh_token = parsed_json['refresh_token']
    file = open("/data/myopentoken.txt", "w")
    file.write(refresh_token)
    file.close()
    file = open("/data/open_tv_token_url.txt", "w")
    file.write("https://www.voicehub.top/api/v1/oauth/alipan/token")
    file.close()


