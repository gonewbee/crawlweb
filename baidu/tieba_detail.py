import requests
from lxml import etree

session = requests.session()
headers = {'User-Agent':
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
session.headers.update(headers)

tieba_base = 'http://tieba.baidu.com'
tieba_home = 'http://tieba.baidu.com/f?'

def get_tieba_url(tieba_name, pn=0):
    '''
    获取百度贴吧内容
    :param tieba_name: 贴吧名称
    :param pn: 帖子的起点
    :return: 获取到的帖子数目
    '''
    params = {'kw': tieba_name, 'ie': 'utf-8', 'pn': pn}
    tieba_url = tieba_home + requests.compat.urlencode(params)
    return tieba_url

def parse_tieba_home_content(content):
    text_remove = content.replace("<!--", "")
    text_remove = text_remove.replace("-->", "")
    page = etree.HTML(text_remove)
    ul_ele = page.find(".//ul[@id='thread_list']")
    li_eles = ul_ele.xpath(".//li[contains(@class, 'j_thread_list')]")
    nums = 0
    for li_ele in li_eles:
        dsts = li_ele.xpath(".//div[contains(@class, 'threadlist_title')]/a")
        if len(dsts) > 0:
            dst = dsts[0]
            # print(dst.attrib)
            print(dst.attrib['title'] + '\t' + tieba_base + dst.attrib['href'])
            nums += 1
    return nums

def parse_tiaba_p_url(url):
    r = session.get(url)
    text_remove = r.text.replace("<!--", "")
    text_remove = text_remove.replace("-->", "")
    page = etree.HTML(text_remove)

def get_tieba_home_content(tieba='济南', pn=0):
    url = get_tieba_url(tieba, pn)
    print(url)
    r = session.get(url)
    parse_tieba_home_content(r.text)

if __name__ == '__main__':
    get_tieba_home_content()
