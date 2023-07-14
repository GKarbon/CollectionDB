# -*- coding: utf-8 -*-
# from urllib.request import urlopen, Request, urlretrieve
import urllib.request as ur
from bs4 import BeautifulSoup
from typing import List, Tuple
import requests
import os

# 指定目标网页的 URL
# url = "https://movie.douban.com/subject/1292064"



def movieCollector(url: str) -> Tuple[str, List[str], List[str], str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "zh-CN",
        "Referer": "https://www.google.com/",
        "Cookie": "cookie1=value1; cookie2=value2",
        "Accept-Charset": "utf-8"
    }

    # 发起请求并获取网页内容
    req = ur.Request(url, headers=headers)
    response = ur.urlopen(req)
    html_content = response.read().decode("utf-8")


    # 解析网页内容
    soup = BeautifulSoup(html_content, "html.parser")
    # print(soup.prettify())

    # 提取电影名
    movie_name_element = soup.find("span", property="v:itemreviewed")
    movie_name = movie_name_element.text if movie_name_element else ""

    # 提取主演信息
    actors = soup.find_all("a", rel="v:starring")
    actor_list = [actor.text for actor in actors]
    actor_list = actor_list[:3] # 只保留前三个主演

    # 提取分类信息
    categories = soup.find_all("span", property="v:genre")
    category_list = [category.text for category in categories]

    # 提取封面图片链接
    img_element = soup.find('img', {'rel': 'v:image'})
    img_url = img_element['src']if img_element else None # type: ignore
    try:
        _, ext = os.path.splitext(img_url) # type: ignore
        # print(ext)
        # print(os.getcwd())
        # print(img_url)    

        response = requests.get(img_url, headers=headers) # type: ignore

        with open(os.path.join(os.path.dirname(__file__)+ f'./{movie_name}'+ ext), 'wb') as f:
            f.write(response.content)
        img_dir =  str(movie_name) + str(ext)
        print(f'图片下载到{img_dir}')
    except:
        img_dir = ""
        print("图片下载失败")

    # 打印提取的信息
    print("电影名:", movie_name)
    print("主演:", ", ".join(actor_list))
    print("分类:", ", ".join(category_list))
    return (movie_name, actor_list, category_list, img_dir)

# movieCollector("https://movie.douban.com/subject/1292064")