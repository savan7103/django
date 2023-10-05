from django.contrib import admin
from .models import User,Artist_profile,Book_Artist

# Register your models here.
admin.site.register(User)
admin.site.register(Artist_profile)
admin.site.register(Book_Artist)
