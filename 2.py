import json
import re
from urllib.parse import quote

import requests
from urllib3 import disable_warnings

query = "和平精英"
clear = "超清"
base_url = "http://haokan.baidu.com/videoui/page/search?pn={}&rn=10&_format=json&tab=video&query={}"
disable_warnings()

ls = []

for i in range(5):
    print(i)
    r = requests.get(base_url.format(i, quote(query)), verify=False)
    for j in r.json().get("data").get("response").get('list'):
        data = {}
        url = j['url']
        title = j['title'].encode("utf-8").decode("utf-8")
        author = str(j['author']).encode("utf-8").decode("utf-8")
        cover = j['cover_src']
        time = str(j["publishTimeText"]).encode("utf-8").decode("utf-8")
        num = str(j["read_num"]).encode("utf-8").decode("utf-8")
        req = requests.get(url.replace('\\', ''), verify=False)
        null = None
        true = True
        false = False
        result = re.search(r"(?<=window.__PRELOADED_STATE__ = ).+(?=document\.querySelector\(\'body\'\))", req.text)
        dic = eval(result.group().replace(" ", "")[:-1])
        if dic.get("curVideoMeta"):
            for k in dic["curVideoMeta"]["clarityUrl"]:
                if k['title'] == clear:
                    video_url = k['url']
        else:
            video_url = None
        data['url'] = url
        data['title'] = title
        data['author'] = author
        data['cover'] = cover
        data['time'] = time
        data['num'] = num
        data['video_url'] = video_url
        ls.append(data)
with open("result.json", "w", encoding="utf-8") as f:
    json.dump(ls, f, indent=4, ensure_ascii=False)
