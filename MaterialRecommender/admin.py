from django.contrib import admin
from .models import *
admin.site.register(Note)
admin.site.register(Todo)
admin.site.register(Contact)
admin.site.register(Member)
admin.site.register(Profile)
# Register your models here.
@admin.register(Material)
class materialAdmin(admin.ModelAdmin):
    list_display=('id','title','categorise','image','content')

@admin.register(Rating)
class ratingAdmin(admin.ModelAdmin):
    list_display=('user','material','rating','rated_date')

