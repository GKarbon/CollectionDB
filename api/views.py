from django.shortcuts import render
from django.http import JsonResponse
from .movieCollector import movieCollector
from MovieCollection.models import Movie, Actor, Category
import json
import os

from django.core.files import File

def crawl_url(request):
    if request.method == 'POST':
        print("Received POST request.")
        # print(request.POST)

        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        
        url = data.get('url')
        # url = request.POST.get('url')
        # if url is None:
        #     return JsonResponse({'error': 'Missing URL parameter.'})
        
        print("Received URL: " + url)
        movie_data = movieCollector(url)  # 调用爬虫脚本获取电影数据

        print(os.path.join(os.path.dirname(__file__), movie_data[3]))

        # 保存电影数据到数据库
        movie = Movie.objects.create(
            title=movie_data[0],
            cover=File(open(os.path.join(os.path.dirname(__file__), movie_data[3]), 'rb'), name=movie_data[3])
            # 其他字段...
        )

        actors = []
        for actor_name in movie_data[1]:
            actor, _ = Actor.objects.get_or_create(name=actor_name)
            actors.append(actor)

        movie.actors.set(actors)

        categories = []
        for category_name in movie_data[2]:
            category, _ = Category.objects.get_or_create(name=category_name)
            categories.append(category)



        movie.category.set(categories)
        
        movie.save()

        os.remove(os.path.join(os.path.dirname(__file__), movie_data[3])) # 删除临时图片文件

        # 返回成功的 JSON 响应
        return JsonResponse({'status': 'success'})
    else:
        # 返回错误的 JSON 响应
        return JsonResponse({'error': 'Invalid request method.'})
