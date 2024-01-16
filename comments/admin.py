from django.contrib import admin

from comments.models import Comment, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email")


admin.site.register(Comment)
