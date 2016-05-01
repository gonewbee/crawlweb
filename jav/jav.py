import requests
import os
import json
import urllib.request
import queue
import threading
from lxml import etree

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
    base_url = ''
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            base_url = json.load(f)['base_url']
    else:
        with open(config_file, 'w') as f:
            base_url = input()
            json.dump({'base_url': base_url}, f)
    return base_url


# 从队列中读取url并操作
def download_worker():
    print('download_worker enter!!!!')
    while True:
        item = _queue.get()
        print(threading.current_thread())
        print('get::' + item)
        if item is None:
            break
        item_file = os.path.join(tmp_path, item.split('/')[-1])
        urllib.request.urlretrieve(item, item_file)
        _queue.task_done()
    print('download_worker end!!!!')


def parse_mostwanted(text):
    page = etree.HTML(text)
    videos = page.xpath("//div[@class='video']")
    for video in videos:
        attrib = video.find("./a").attrib
        image_src = video.find(".//img").attrib['src']
        print(attrib)
        print('put::' + image_src)
        _queue.put(image_src)

def start_download_thread():
    for i in range(num_worker_threads):
        t = threading.Thread(target=download_worker())
        t.start()
        threads.append(t)

def join_down_thread():
    for i in range(num_worker_threads):
        _queue.put(None)
    # 等待队列结束
    _queue.join()
    # 等待线程结束
    for t in threads:
        t.join()


def get_mostwanted(mode=None, page=None):
    params = {}
    if mode is not None:
        params['mode'] = mode
    if page is not None:
        params['page'] = page
    base_url = get_jav_base_url()
    mostwanted_url = base_url + '/vl_mostwanted.php'
    if len(params) != 0:
        mostwanted_url = mostwanted_url + '?' + requests.compat.urlencode(params)
    print(mostwanted_url)
    session = requests.session()
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.81 Safari/537.36'}
    proxies = {'http': '127.0.0.1:8087'}
    r = session.get(mostwanted_url, headers=headers, proxies=proxies)
    parse_mostwanted(r.text)


if __name__ == '__main__':
    get_mostwanted()
    start_download_thread()
    join_down_thread()

