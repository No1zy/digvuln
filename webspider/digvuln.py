import requests
import sys
import re
import os
import argparse
import json
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
parser.add_argument('--store', '-s', help='store XSS sink URL')
args = parser.parse_args()


class digVuln():

    def __init__(self, url):
        self.url = url
        self.target = None
        self.cookies = None
        self.method = "POST"

    #ログインする
    # @param dict payload
    # @return cookie　ログインできなかったらFalse
    def login(self, payload):
        login_url = self.url + "/login.php"
        command = 'scrapy crawl login -a data="{0}" -a target="{1}" -o session.json --nolog'.format(payload, login_url)
        os.system(command)
        f = open("session.json", "r")
        target_list = f.read()
        f.close()
        os.system("rm -f session.json")
        self.cookies = json.loads(target_list)[0]['cookies']
        if self.cookies == None:
            return False
        return True

    #引数のデータを分割する
    # @param string data
    # @return dict payload
    def split_data(self, data):
        tmp = data.split("&")
        payload = dict()
        for param in tmp:
            key, value = param.split("=")
            data = {key: value}
            payload.update(data)
        return payload

    def is_current_dir(self, path):
        current_patte = "^\.\/.*|^(?!.*\/).*$"
        current_dir_reg = re.compile(current_patte)
        return True if current_dir_reg.match(path) else False

    #結果を表示
    # @param dict payload
    #        string target
    # @return void
    def print_vuln(self, place, target):
        print(FAIL + "Vulnable!!" + ENDC)
        print(WARNING + "send payload" + ENDC)
        print(WARNING + "\t" + str(place) + ENDC)
        #print("\t" + place)

    #リクエストパラメータを探索＆追加処理
    def dig_param(self):
        r = requests.get(self.target, cookies=self.cookies)
        bs = BeautifulSoup(r.text, "html.parser")
        forms = bs.find_all("form")
        payload = dict()
        for elm in forms:
            self.method = elm.get("method") if elm.get("method") else "get"  # HTTPメソッド
            bs = BeautifulSoup(str(elm), "html.parser")
            children = bs.find_all()
            for child in children:
                name = child.get("name")
                #タグにname属性があったら
                if name is not None:
                    if child.option:
                        tmp = {name: child.option.get("value") if child.option.get("value") else ''}
                    else:
                        tmp = {name: child.get("value") if child.get("value") else ''}
                    #リクエストパラメータに追加
                    payload.update(tmp)
        return payload

    # ターゲットリストを作成
    def make_list(self):
        if self.cookies:
            for key , value in self.cookies.items():
                command = 'scrapy crawl web_spider -a target="{0}" -a cookie="{1}={2}" -o target.json --nolog'.format(self.url, key, value)
        else:
            command = 'scrapy crawl web_spider -a target="{0}" -o target.json --nolog'.format(self.url)
        os.system(command) 
        f = open("target.json","r")
        target_list = f.read()
        f.close()
        os.system("rm -f target.json")
        return json.loads(target_list)
               
    def select_target(self, link_list):
        i = 1  # ターゲットリストのindex
        # ターゲットリストが1以上だったら
        if len(link_list) > 0:
            print(OKBLUE + "Please select Target." + ENDC)
            for link in link_list:
                print("[" + str(i) + "] => " + link['urls'])
                i += 1
            number = input("Number : ")     # ターゲットの番号
            if len(number) < 1 or int(number) - 1 >= len(link_list):
                print(FAIL + "Out of range number" + ENDC)
                exit(2)
            number = int(number) - 1
            #生成するURLを分ける
            self.target = link_list[number]['urls']
            print(FAIL + "Target url : " + ENDC + self.target + "\n")

    def attack(self, payload, store_sink):
        file_list = ["etc/xss.txt"]
        #XSS診断
        flag = False  # 診断可否フラグ
        for key, value in payload.items():
            for file_name in file_list:
                with open(file_name, "r") as f:
                    attack = True  # xss ペイロード
                    while flag != True and attack:
                        attack = f.readline()
                        payload[key] = attack
                        print(payload )
                        if self.method.lower() == "get":
                            r = requests.get(self.target, params=payload, cookies=self.cookies)
                        else:
                            r = requests.post(self.target, data=payload, cookies=self.cookies)
                        # storeオプションが設定されていたら指定されたURLを見にいく
                        if store_sink is not None:
                            payload = digvuln.dig_param()
                            r = requests.get(store_sink, params=payload, cookies=self.cookies)
                        bs = BeautifulSoup(r.text, "html.parser")
                        list_all = bs.find_all()
                        for elm in list_all:
                            if str(elm) in attack:
                                digvuln.print_vuln(payload, self.target)
                                flag = True
                        #payloadを元に戻す
                        payload[key] = value
        if flag is False:
            print(OKGREEN + "Not found vulnerability" + ENDC)

    def run(self):
        target_list = digvuln.make_list()
        digvuln.select_target(target_list)
        payload = digvuln.dig_param()
        query_reg = re.compile(r".*\?.*")
        if self.method.lower() == "get" or query_reg.match(self.target):
            query = self.target.split("?")
            params = self.split_data(query[1])
            payload.update(params)
            self.method = "get"
        digvuln.attack(payload, store_sink)

if __name__ == '__main__':
    url = args.url
    login_data = args.login
    store_sink = args.store
    cookies = ""

    digvuln = digVuln(url)
    # loginオプションが設定されていたら
    if login_data is not None:
        if digvuln.login(login_data) == False:
            print(FAIL + "Login falied..." + ENDC)
            exit(2)
    digvuln.run()
