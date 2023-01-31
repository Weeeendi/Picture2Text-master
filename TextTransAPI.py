# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

from ctypes.wintypes import WORD
from enum import auto
from importlib.machinery import WindowsRegistryFinder
import requests
import random
from hashlib import md5

# Set your own appid/appkey.
appid = '20210422000794630'
appkey = 'Cp7G1L9U12aRsx3_tk2c'

# For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
from_lang = 'auto'
to_lang =  'zh'

endpoint = 'http://api.fanyi.baidu.com'
path = '/api/trans/vip/translate'
url = endpoint + path

#query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'

# Generate salt and sign
def make_md5(s, encoding='utf-8'):
    return md5(s.encode(encoding)).hexdigest()

def TextTranslate(to_lang,srcText,from_lang = 'auto'):
    r"""Translate src text to dst text.

    :param from_lang: auto,en,zh.....
    :param to_lang: en.zh.....
    :param srcText: need to translate texts
    :return dstTest: translated texts to aim langurge 
    """

    salt = random.randint(32768, 65536)
    sign = make_md5(appid + srcText + str(salt) + appkey)

    # Build request
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    payload = {'appid': appid, 'q': srcText, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    r = requests.post(url, params=payload, headers=headers)
    result = r.json()
    words = ""
    
    for item in result['trans_result']:
        words += (item.get('dst')+'\n')
    return words

# Show response
#print(json.dumps(result, indent=4, ensure_ascii=False))


#print(TextTranslate('en',"我爱你中国\n 你是我的母亲"))