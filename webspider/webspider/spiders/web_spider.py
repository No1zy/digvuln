# -*- coding: utf-8 -*-

import scrapy
import sys
class webSpider(scrapy.Spider):
    name = 'web_spider'
    # エンドポイント（クローリングを開始するURLを記載する）

    custom_settings = {
        "DOWNLOAD_DELAY": 1,
    }

    def start_requests(self):

        url = ""
        cookies = None
        # コマンドラインから渡した引数は、デフォルトでSpiderのアトリビュートとして取得することができます。
        # 今回の場合、self.categoriesで引数の値を取得できます。
        target = getattr(self, 'target', None)
        cookie = getattr(self, 'cookie', None)
        if target:
            url = '{0}'.format(target)
            
        if cookie:
            cookies = self.split_data(cookie)
        yield scrapy.Request(url, self.parse, cookies=cookies)

    #引数のデータを分割する
    # @param string data
    # @return dict payload
    def split_data(self, data):
        payload = dict()
        key, value = data.split("=")
        data = {key: value}
        payload.update(data)
        return payload

    # コマンドラインから渡した引数は、デフォルトでSpiderのアトリビュートとして取得することができます。
    # 今回の場合、self.categoriesで引数の値を取得できます。

    # URLの抽出処理を記載
    def parse(self, response):
        for href in response.css('a::attr(href)'):
            full_url = response.urljoin(href.extract())
            # 抽出したURLを元にRequestを作成し、ダウンロードする
            yield {
                'urls' : full_url,
            }
