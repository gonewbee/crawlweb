import requests
import os
import json
import urllib.request
import queue
import threading
from lxml import etree

session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
proxies = {'http': '127.0.0.1:8087'}
# 线程数目
num_worker_threads = 5
_queue = queue.Queue()
threads = []
file_path = os.path.dirname(os.path.abspath(__file__))
tmp_path = os.path.join(file_path, 'tmp')
if not os.path.exists(tmp_path):
    os.makedirs(tmp_path)


def get_jav_base_url():
    config_file = os.path.join(file_path, 'config.json')
    _base_url = ''
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            _base_url = json.load(f)['base_url']
    else:
        with open(config_file, 'w') as f:
            _base_url = input('enter url:')
            json.dump({'base_url': _base_url}, f)
    return _base_url


base_url = get_jav_base_url()


def get_videocomments(videocomments_url):
    comments = []
    for i in range(1, 3):
        _url = videocomments_url + '&page=' + str(i)
        r = session.get(_url, headers=headers, proxies=proxies)
        page = etree.HTML(r.text)
        texts = page.xpath("//textarea")
        for text in texts:
            comment = text.xpath("string()")
            if comment.find('中文') > 0:
                comments.append(comment)
    if len(comments) > 0:
        print(videocomments_url + '::::' + str(comments))


# 从队列中读取url并操作
def download_worker():
    print('download_worker enter!!!!')
    while True:
        item = _queue.get()
        if item is None:
            break
        print('get::' + str(item))
        get_videocomments(item['href'])
        image_src = item['image_src']
        image_file = os.path.join(tmp_path, image_src.split('/')[-1])
        urllib.request.urlretrieve(image_src, image_file)
        _queue.task_done()
    print(str(threading.current_thread()) + '::download_worker end!!!!')


def parse_mostwanted(text):
    page = etree.HTML(text)
    videos = page.xpath("//div[@class='video']")
    for video in videos:
        attrib = video.find("./a").attrib
        image_src = video.find(".//img").attrib['src']
        print(attrib)
        href = base_url + '/videocomments.php' + attrib['href'].split('/')[-1]
        _queue.put({'href': href, 'image_src': image_src})


def start_download_thread():
    '''
    启动下载线程
    '''
    for i in range(num_worker_threads):
        t = threading.Thread(target=download_worker)
        t.start()
        threads.append(t)


def join_down_thread():
    '''
    结束下载线程
    '''
    # 等待队列结束
    _queue.join()
    for i in range(num_worker_threads):
        _queue.put(None)
    print("queue join!!!")
    # 等待线程结束
    for t in threads:
        t.join()
    print("threads join!!!")


def get_mostwanted(mode=None, page=None):
    params = {}
    if mode is not None:
        params['mode'] = mode
    if page is not None:
        params['page'] = page
    mostwanted_url = base_url + '/vl_mostwanted.php'
    if len(params) != 0:
        mostwanted_url = mostwanted_url + '?' + requests.compat.urlencode(params)
    print(mostwanted_url)
    r = session.get(mostwanted_url, headers=headers, proxies=proxies)
    parse_mostwanted(r.text)


if __name__ == '__main__':
    import sys

    start_download_thread()
    if len(sys.argv) > 1:
        nums = int(sys.argv[1])
        for i in range(1, nums + 1):
            get_mostwanted(page=i)
    else:
        get_mostwanted()
    join_down_thread()

