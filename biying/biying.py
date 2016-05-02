import requests
from lxml import etree


def search(key):
    search_url = 'http://cn.bing.com/search?'
    keys = {'q': key}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    url = search_url + requests.compat.urlencode(keys)
    r = requests.get(url, headers=headers)
    list_result(r.text)


def list_result(html):
    page = etree.HTML(html)
    # 找出所有的ol下的li
    results = page.xpath('//ol/li')
    for result in results:
        # 加点（.//）在当前元素下查找
        contents = result.xpath('.//h2/a')
        for con in contents:
            print(con.xpath('string()'))
            print(con.attrib['href'], end='\n\n')

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        with open('test.html', 'r') as f:
            d = f.read()
            list_result(d)
    else:
        search(sys.argv[1])
