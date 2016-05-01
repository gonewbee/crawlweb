# coding: utf-8
import requests
from lxml import etree


def get_tieba_url(tieba_url):
    session = requests.session()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    url_parse = requests.compat.urlparse(tieba_url)
    base_url = url_parse.scheme + '://' + url_parse.netloc
    r = session.get(tieba_url, headers=headers)
    # 删除贴吧中的注释"<!--"
    text_remove = r.text.replace("<!--", "")
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
            print(dst.attrib['title'] + '\t' + base_url + dst.attrib['href'])
            nums += 1
    return nums


def get_teiba_name_pn(tieba_name, pn=0):
    '''
    获取百度贴吧内容
    :param tieba_name: 贴吧名称
    :param pn: 帖子的起点
    :return: 获取到的帖子数目
    '''
    params = {'kw': tieba_name, 'ie': 'utf-8', 'pn': pn}
    tieba_url = 'http://tieba.baidu.com/f?' + requests.compat.urlencode(params)
    return get_tieba_url(tieba_url)


if __name__ == '__main__':
    import sys

    argv_len = len(sys.argv)
    if argv_len == 1:
        # 济南吧
        # nums = get_tieba_url('http://tieba.baidu.com/f?kw=%E6%B5%8E%E5%8D%97&ie=utf-8&pn=0')
        nums = get_teiba_name_pn('济南')
        print('get nums:%d' % (nums))
    elif argv_len == 2:
        get_teiba_name_pn(sys.argv[1])
    else:
        get_teiba_name_pn(sys.argv[1], sys.argv[2])
