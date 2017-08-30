import requests
import sys
import re
import argparse
from bs4 import BeautifulSoup

OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"

#オプション設定
parser = argparse.ArgumentParser()
parser.add_argument('url', help='Scan URL')
parser.add_argument('--login', '-l', help='Login data')
args = parser.parse_args()

#ログインする
# @param dict payload    
# @return cookie　ログインできなかったらFalse
def login(payload):
    login = url + "/login.php"
    r = requests.post(login, data=payload, allow_redirects=False)
    if r.text in "Logout":
        return r.cookies
    return False

#引数のデータを分割する
# @param string data
# @return dict payload
def split_data(data):
    tmp = data.split("&")
    payload = dict()
    for param in tmp:
        key, value = param.split("=")
        data = {key: value}
        payload.update(data)
    return payload

#結果を表示
# @param dict payload
#        string target
# @return void
def print_vuln(payload, target):
    print(FAIL + "Vulnable!!" + ENDC)
    print(WARNING + "Request params" + ENDC)
    for key, val in payload.items():
        print("\t" + key + " : " + val)


url = args.url
login_data = args.login
cookies = ""

# loginオプションが設定されていたら
if login_data is not None:
    payload = split_data(login_data)
    cookies = login(payload)
    if cookies == False:
        print(FAIL + "Login falied..." + ENDC)
        exit(2)

# ターゲットリストを作成
r = requests.get(url, cookies=cookies)
bs = BeautifulSoup(r.text, "html.parser")
links = bs.find_all("a")
link_list = list()
for link in links:
    href = link.get("href")
    if href is None:
        continue
    link_list.append(href)
target = url


i = 1    #ターゲットリストのindex
# ターゲットリストが1以上だったら
if len(link_list) > 0:
    print(OKBLUE + "Please select Target." + ENDC)
    for link in link_list:
        print("[" + str(i) + "] => " + str(link))
        i += 1
    number = input("Number : ")     # ターゲットの番号
    if len(number) < 1 or int(number) - 1 >= len(link_list):
        print(FAIL + "Out of range number" + ENDC)
        exit(2)
    number = int(number) - 1
    target = url + link_list[number]
    print(FAIL + "Target url : " + ENDC + target + "\n")

#リクエストパラメータを探索＆追加処理
r = requests.get(target, cookies=cookies)
bs = BeautifulSoup(r.text, "html.parser")
forms = bs.find_all("form")
payload = dict()
for elm in forms:
    method = elm.get("method") if elm.get("method") else "get"     #HTTPメソッド
    bs = BeautifulSoup(str(elm), "html.parser")
    children = bs.find_all()
    for child in children:
        name = child.get("name")
        #タグにname属性があったら
        if name is not None:
            if child.option:
                tmp = {name: child.option.get(
                    "value") if child.option.get("value") else ''}
            else:
                tmp = {name: child.get("value") if child.get("value") else ''}
            #リクエストパラメータに追加
            payload.update(tmp)

#XSS診断
for key, value in payload.items():
    with open("xss.txt", "r") as f:
        xss = True    #xss ペイロード
        flag = False  #診断可否フラグ
        while flag != True and xss:
            xss = f.readline()
            payload[key] = xss

            r = requests.post(target, data=payload, cookies=cookies)
            #TODO: ストア型XSSの判断処理の実装
            #r = requests.get(index, cookies=cookies)
            bs = BeautifulSoup(r.text, "html.parser")
            #a = bs.find("a", href=re.compile(".*readdiary.*"))
            #href = a.get("href")
            #r = requests.get(url + target, cookies=cookies)
            #bs = BeautifulSoup(r.text, "html.parser")
            list_all = bs.find_all()
            for elm in list_all:
                if str(elm) in xss:
                    print_vuln(payload, target)
                    flag = True
            #restore payload
            payload[key] = value
