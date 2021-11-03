#!/usr/bin/env python
# coding:utf-8
from hashlib import md5

from tool.async_base_httpx import AsyncBaseHttpx


class Chaojiying_Client(AsyncBaseHttpx):
    def __init__(self, username, password, soft_id):
        super().__init__('cjy')
        self.username = username
        password = password.encode('utf8')
        self.password = md5(password).hexdigest()
        self.soft_id = soft_id
        self.base_params = {
            'user': self.username,
            'pass2': self.password,
            'softid': self.soft_id,
        }
        self.headers = {
            'Connection': 'Keep-Alive',
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0)',
        }

    async def PostPic(self, img, codetype=9101):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        # im = open(file, 'rb').read()
        params = {
            'codetype': codetype,
        }
        params.update(self.base_params)
        files = {'userfile': ('ccc.jpg', img)}
        # async with aiohttp.ClientSession() as session:
        resp = await self.session.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, files=files,
                                       headers=self.headers)
        res = await resp.json()
        if res['err_str'] == 'OK':
            x_code = res['pic_str']
            self.im = res['pic_id']
            # print(x_code)
            return x_code
        elif res['err_str'] == '无可用题分':
            raise Exception('超级鹰没钱啦！')
        else:
            x_code = self.PostPic(img, codetype=codetype)
            return x_code

    async def PostPic_base64(self, img, codetype=9101):
        """
        im: 图片字节
        codetype: 题目类型 参考 http://www.chaojiying.com/price.html
        """
        # im = open(file, 'rb').read()
        params = {
            'codetype': codetype,
            'file_base64': img
        }
        params.update(self.base_params)
        # params = json.dumps(params)
        res = await self.session.post('http://upload.chaojiying.net/Upload/Processing.php', data=params,
                                      headers=self.headers)
        res = res.json()
        # async with aiohttp.ClientSession() as session:
        #     async with session.post('http://upload.chaojiying.net/Upload/Processing.php', data=params, headers=self.headers) as resp:
        #         res = await resp.json()
        if res['err_str'] == 'OK':
            x_code = res['pic_str']
            self.im = res['pic_id']
            # print(x_code)
            return x_code
        else:
            x_code = await self.PostPic_base64(img, codetype=codetype)
            return x_code

    async def ReportError(self):
        """
        im_id:报错题目的图片ID
        """
        params = {
            'id': self.im,
        }
        params.update(self.base_params)
        res = await self.session.post('http://upload.chaojiying.net/Upload/Processing.php', data=params,
                                      headers=self.headers)
        res_text = res.json()
        print('执行报错')
        return res_text


if __name__ == '__main__':
    chaojiying = Chaojiying_Client('9007789', 'mengyongb', '9101')  # 用户中心>>软件ID 生成一个替换 96001
    # 本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
    print(chaojiying.PostPic('text.png', 9101))  # 1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()
