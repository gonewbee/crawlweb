__author__ = 'zhangshy'
import requests
import json

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
cookies = {
    "destLang": "zh-CHS",
    "dmru_list": "da%2Czh-CHS",
    "destDia": "zh-CN",
    "srcLang": "en",
    "smru_list": "en",
    "sourceDia": "en-US",
    "SRCHD": "AF=NOFORM",
    "SRCHUSR": "DOB=20160502",
    "_EDGE_V": "1",
    "MUID": "2696DCA3568B6D6F3B9BD5AA572A6CB8",
    "_EDGE_S": "mkt=zh-cn&SID=2FF17396A9C761041BF27A9FA86660EE",
    "SRCHHPGUSR": "CW=1903&CH=979&DPR=1",
    "_SS=SID": "2FF17396A9C761041BF27A9FA86660EE&HV=1462196420&bIm=624",
    "mtstkn": "hzeXs5uHIrN8lzBEVFdXPHq%2BKP3cXDdTebB7F0pkdX87imsS%2FPHiPpFyYJY4PtXv",
    "MUIDB": "2696DCA3568B6D6F3B9BD5AA572A6CB8",
    "SNRHOP": "I=&TS=",
    "SRCHUID": "V=2&GUID=43E4B6E30A2F4F1EB4D0088100FCF614",
    "WLS": "C=&N="}
session.headers.update(headers)
session.cookies.update(cookies)


def en2ch(word):
    en2ch_url = 'http://www.bing.com/translator/api/Dictionary/Lookup?from=en&to=zh-CHS&' + \
                requests.compat.urlencode({'text': word})
    r = session.get(en2ch_url)
    ret = json.loads(r.text)
    for item in ret['items'][0]:
        print(item['normalizedTarget'])


if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        en2ch('python')
    else:
        en2ch(sys.argv[1])
