import requests
import base64
import io
from PIL import Image

def get_challenge_list():  # 获取今日的赛题，以列表方式展示所有的赛题
    url = 'http://47.102.118.1:8089/api/challenge/list'
    html = requests.get(url)  # 获取json文件
    html_json = html.json()
    print(html_json)
    return html_json

def get_challenge_record(uuid):  # 获取赛题的解题记录，返回所有解出这题的队伍的纪录
    url = 'http://47.102.118.1:8089/api/challenge/record/'
    url = url + uuid
    html = requests.get(url)  # 获取json文件
    html_json = html.json()
    print(html_json)

def creat():
    url = 'http://47.102.118.1:8089/api/challenge/create'
    data = {
        "teamid": 57,
        "data": {
            "letter": "t",
            "exclude": 8,
            "challenge": [
                [1, 3, 5],
                [7, 0, 9],
                [2, 6, 4]
            ],
            "step": 9,
            "swap": [2, 3]
        },
        "token": "965d5fbe-4e91-4a89-9f97-fdbe611ecd5a"
    }
    r = requests.post(url, json=data)
    r_json = r.json()
    # 'uuid': '1058aabd-d1bc-43f8-af23-f87faf4f8b2c'
    print(r_json)

def start(uuid):
    url = 'http://47.102.118.1:8089/api/challenge/start/' + uuid
    teamdata = {
        "teamid": 57,
        "token": "965d5fbe-4e91-4a89-9f97-fdbe611ecd5a"
    }
    r = requests.post(url, json=teamdata)
    r_json = r.json()
    print(r_json)
    chanceleft = r_json['chanceleft']
    img_str = r_json['data']['img']
    step = r_json['data']['step']
    swap = r_json['data']['swap']
    uuid = r_json['uuid']
    img_b64decode = base64.b64decode(img_str)  # base64解码
    file = open('test.jpg', 'wb')
    file.write(img_b64decode)
    file.close()
    image = io.BytesIO(img_b64decode)
    img = Image.open(image)
    return img, step, swap, uuid

def up_data(uuid, answer):
    url_up = 'http://47.102.118.1:8089/api/challenge/submit'
    updata = {
        "uuid": uuid,
        "teamid": 57,
        "token": "965d5fbe-4e91-4a89-9f97-fdbe611ecd5a",
        "answer": {
            "operations": answer,
            "swap": []
        }
    }
    r_up = requests.post(url_up, json=updata)
    r_up_json = r_up.json()
    print(r_up_json)

def get_rank():
    url_rank = 'http://47.102.118.1:8089/api/rank'
    html = requests.get(url_rank)  # 获取json文件
    html_json = html.json()
    print(html_json)
    rank_list = []

challenge_list = get_challenge_list()
uuid_list = []
for i in range(len(challenge_list)):
    uuid_list.append(challenge_list[i]['uuid'])
f = open('uuid.txt', 'w')
for i in uuid_list:
    f.write(i + '\n')
f.close()
# creat()
# get_challenge_record(uuid)
# print(uuid)
# img, step, swap, uuid = start(uuid)
# print(img, step, swap, uuid)
uuid = "d611e470-e052-4802-870a-4500544986de"
answer = "wswswswswswswswsdwwassawdsdwawdsaasdd"
# up_data(uuid, answer)
get_rank()