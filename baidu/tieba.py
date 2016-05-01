# coding: utf-8
import requests
from lxml import etree

def get_tieba_url(tieba_url):
    session = requests.session()
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    url_parse = requests.compat.urlparse(tieba_url)
    base_url = url_parse.scheme + '://' + url_parse.netloc
    r = session.get(tieba_url, headers=headers)
    # 删除贴吧中的注释"<!--"
    text_remove = r.text.replace("<!--", "")
    text_remove = text_remove.replace("-->", "")

    page = etree.HTML(text_remove)
    tags = page.xpath("//ul[@id='thread_list']/li")
    # tags[1].xpath("string()").split()
    for tag in tags:
        dst = tag.xpath(".//div[contains(@class, 'threadlist_title')]/a")[0]
        # print(dst.attrib)
        print(dst.attrib['title'] + '\t' + base_url+dst.attrib['href'])


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        # 济南吧
        get_tieba_url('http://tieba.baidu.com/f?kw=%BC%C3%C4%CF&fr=ala0&tpl=5')
    else:
        get_tieba_url(sys.argv[1])
