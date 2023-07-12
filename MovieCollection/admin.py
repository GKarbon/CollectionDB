from django.contrib import admin
from .models import Movie, Actor, Category

class ActorAdmin(admin.ModelAdmin):
    pass

class CategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(Movie)
admin.site.register(Actor, ActorAdmin)
admin.site.register(Category, CategoryAdmin)