from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Movie, Actor, Category

class MovieModelTestCase(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Action')
        self.actor = Actor.objects.create(name='Tom Hanks')
        self.movie = Movie.objects.create(
            title='Forrest Gump',
            cover=SimpleUploadedFile('cover.jpg', b'content'),
        )
        self.movie.category.add(self.category)
        self.movie.actors.add(self.actor)
    
    def test_movie_str(self):
        self.assertEqual(str(self.movie), 'Forrest Gump')
    
    def test_movie_category(self):
        self.assertEqual(self.movie.category.count(), 1)
        self.assertEqual(self.movie.category.first(), self.category)
    
    def test_movie_actors(self):
        self.assertEqual(self.movie.actors.count(), 1)
        self.assertEqual(self.movie.actors.first(), self.actor)
    
    def test_actor_str(self):
        self.assertEqual(str(self.actor), 'Tom Hanks')
    
    def test_category_str(self):
        self.assertEqual(str(self.category), 'Action')


class MovieListViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('movies')
        self.movie1 = Movie.objects.create(title='Forrest Gump')
        self.movie2 = Movie.objects.create(title='The Shawshank Redemption')
    
    def test_movie_list_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'movies.html')
        self.assertContains(response, self.movie1.title)
        self.assertContains(response, self.movie2.title)

if __name__ == "__main__":
    MovieModelTestCase().test_movie_str()
    MovieModelTestCase().test_movie_category()
    MovieModelTestCase().test_movie_actors()
    MovieModelTestCase().test_actor_str()
    MovieModelTestCase().test_category_str()