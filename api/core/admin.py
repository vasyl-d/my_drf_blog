from django.contrib import admin

# Register your models here.
from .models import Post, Tag, FeedBack, Comment

class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'url': ('name',)}


admin.site.register(Post, PostAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(FeedBack)
admin.site.register(Comment)