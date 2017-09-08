import scrapy

class LoginSpider(scrapy.Spider):
    name = 'login'
    start_urls = []

    def start_requests(self):

        meta_data = { 
                 'dont_redirect' : True,
                 'handle_httpstatus_list': [302],
             } 
        url = ""
        # コマンドラインから渡した引数は、デフォルトでSpiderのアトリビュートとして取得することができます。
        # 今回の場合、self.categoriesで引数の値を取得できます。
        target = getattr(self, 'target', None)
        if target:
            url = '{0}'.format(target)
        yield scrapy.Request(url, self.parse, meta=meta_data)

    def parse(self, response):
        data = getattr(self, 'data', None)
        payload = self.split_data(data)
        meta_data = { 
                 'dont_redirect' : True,
                 'handle_httpstatus_list': [302],
             } 
        return scrapy.FormRequest.from_response(
            response,
            formdata=payload,
            callback=self.after_login,
            meta=meta_data,
        )

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

    #引数のデータを分割する
    # @param string data
    # @return dict payload
    def split_cookies(self, data):
        tmp = data.split("; ")
        payload = dict()
        items = tmp[0].split("=")
        if len(items) > 1:
            data = {items[0] : items[1]}
            payload.update(data)
        return payload

    def after_login(self, response):
        # check login succeed before going on
        #if "authentication failed" in response.body:
        #    self.logger.error("Login failed")
        #    return
        session_id = "".join([chr(x) for x in response.headers.getlist('Set-Cookie')[0]])
        session_id = self.split_cookies(session_id)
        yield {'cookies' : session_id}
