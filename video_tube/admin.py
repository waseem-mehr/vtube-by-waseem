from django.contrib import admin
from .models import UserModel,Commment,Video,Categorey,Like,Unlike,Reply,Views
# Register your models here.
admin.site.register(UserModel)
admin.site.register(Categorey)
admin.site.register(Video)
admin.site.register(Commment)
admin.site.register(Reply)
admin.site.register(Like)
admin.site.register(Unlike)
admin.site.register(Views)

