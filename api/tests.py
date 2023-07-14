from django.test import TestCase, Client
from django.urls import reverse
from unittest import mock
from douBanMovieCollector import movieCollector
import io
import os

class MovieCollectorTestCase(TestCase):
    @mock.patch('builtins.print')
    @mock.patch('urllib.request.urlopen')
    def test_movieCollector(self, mock_urlopen, mock_print):
        # 模拟 urlopen 的返回值
        mock_urlopen.return_value = io.BytesIO('''
            <!DOCTYPE html>
            <html lang="zh-CN" class="ua-windows ua-webkit">
            <head>
                <title>
                    肖申克的救赎 (豆瓣)
                </title>
            </head>

            <body>

                <h1>
                    <span property="v:itemreviewed">肖申克的救赎 The Shawshank Redemption</span>
                        <span class="year">(1994)</span>
                </h1>

                <div id="mainpic" class="">
                    <a class="nbgnbg" href="https://movie.douban.com/subject/1292052/photos?type=R" title="点击看更多海报">
                        <img src="https://img2.doubanio.com/view/photo/s_ratio_poster/public/p480747492.webp" title="点击看更多海报" alt="The Shawshank Redemption" rel="v:image" />
                </a>
                </div>

                <div id="info">
                    <span ><span class='pl'>导演</span>: <span class='attrs'><a href="/celebrity/1047973/" rel="v:directedBy">弗兰克·德拉邦特</a></span></span><br/>
                    <span ><span class='pl'>编剧</span>: <span class='attrs'><a href="/celebrity/1047973/">弗兰克·德拉邦特</a> / <a href="/celebrity/1049547/">斯蒂芬·金</a></span></span><br/>
                    <span class="actor"><span class='pl'>主演</span>: <span class='attrs'><a href="/celebrity/1054521/" rel="v:starring">蒂姆·罗宾斯</a> / <a href="/celebrity/1054534/" rel="v:starring">摩根·弗里曼</a> / <a href="/celebrity/1041179/" rel="v:starring">鲍勃·冈顿</a> / <a href="/celebrity/1000095/" rel="v:starring">威廉姆·赛德勒</a> / <a href="/celebrity/1013817/" rel="v:starring">克兰西·布朗</a> / <a href="/celebrity/1010612/" rel="v:starring">吉尔·贝罗斯</a> / <a href="/celebrity/1054892/" rel="v:starring">马克·罗斯顿</a> / <a href="/celebrity/1027897/" rel="v:starring">詹姆斯·惠特摩</a> / <a href="/celebrity/1087302/" rel="v:starring">杰弗里·德曼</a> / <a href="/celebrity/1074035/" rel="v:starring">拉里·布兰登伯格</a> / <a href="/celebrity/1099030/" rel="v:starring">尼尔·吉恩托利</a> / <a href="/celebrity/1343305/" rel="v:starring">布赖恩·利比</a> / <a href="/celebrity/1048222/" rel="v:starring">大卫·普罗瓦尔</a> / <a href="/celebrity/1343306/" rel="v:starring">约瑟夫·劳格诺</a> / <a href="/celebrity/1315528/" rel="v:starring">祖德·塞克利拉</a> / <a href="/celebrity/1014040/" rel="v:starring">保罗·麦克兰尼</a> / <a href="/celebrity/1390795/" rel="v:starring">芮妮·布莱恩</a> / <a href="/celebrity/1083603/" rel="v:starring">阿方索·弗里曼</a> / <a href="/celebrity/1330490/" rel="v:starring">V·J·福斯特</a> / <a href="/celebrity/1000635/" rel="v:starring">弗兰克·梅德拉诺</a> / <a href="/celebrity/1390797/" rel="v:starring">马克·迈尔斯</a> / <a href="/celebrity/1150160/" rel="v:starring">尼尔·萨默斯</a> / <a href="/celebrity/1048233/" rel="v:starring">耐德·巴拉米</a> / <a href="/celebrity/1000721/" rel="v:starring">布赖恩·戴拉特</a> / <a href="/celebrity/1333685/" rel="v:starring">唐·麦克马纳斯</a></span></span><br/>
                    <span class="pl">类型:</span> <span property="v:genre">剧情</span> / <span property="v:genre">犯罪</span><br/>
                    <span class="pl">制片国家/地区:</span> 美国<br/>
                    <span class="pl">语言:</span> 英语<br/>
                    <span class="pl">上映日期:</span> <span property="v:initialReleaseDate" content="1994-09-10(多伦多电影节)">1994-09-10(多伦多电影节)</span> / <span property="v:initialReleaseDate" content="1994-10-14(美国)">1994-10-14(美国)</span><br/>
                    <span class="pl">片长:</span> <span property="v:runtime" content="142">142分钟</span><br/>
                    <span class="pl">又名:</span> 月黑高飞(港) / 刺激1995(台) / 地狱诺言 / 铁窗岁月 / 消香克的救赎<br/>
                    <span class="pl">IMDb:</span> tt0111161<br>
                </div>

            <body>

            </html>
            '''.encode('utf-8'))

        url = "https://movie.douban.com/subject/1292052"
        expected_output = ("肖申克的救赎 The Shawshank Redemption", ["蒂姆·罗宾斯", "摩根·弗里曼", "鲍勃·冈顿"], ["剧情", "犯罪"], "肖申克的救赎 The Shawshank Redemption.webp")
        self.assertEqual(movieCollector(url), expected_output)
        os.remove(os.path.join(os.path.dirname(__file__),"肖申克的救赎 The Shawshank Redemption.webp"))

class CrawlURLViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('api:crawl_url')
    
    def test_crawl_url_success(self):
        print(self.url)
        print(self.client)
        # Test crawling a valid URL
        response = self.client.post(self.url, {'url': 'https://www.example.com'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'status': 'success'})
    
    def test_crawl_url_invalid_method(self):
        # Test using an invalid HTTP method
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 405)
    
    def test_crawl_url_missing_parameter(self):
        # Test missing the 'url' parameter
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Missing required parameter: url'})
    
    def test_crawl_url_invalid_url(self):
        # Test crawling an invalid URL
        response = self.client.post(self.url, {'url': 'not_a_url'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Invalid URL'})

if __name__ == "__main__":
    MovieCollectorTestCase().test_movieCollector()
    CrawlURLViewTestCase().setUp()
