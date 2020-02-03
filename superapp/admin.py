from django.contrib import admin

# Register your models here.
from .models import AboutStartup,StartupGroup,UserProfile,Post
admin.site.register(AboutStartup)
admin.site.register(StartupGroup)
admin.site.register(UserProfile)
admin.site.register(Post)
