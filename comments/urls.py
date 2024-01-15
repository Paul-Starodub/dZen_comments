from django.urls import path

from comments.views import add_comment, comment_detail, comment_list


urlpatterns = [
    path("add/", add_comment, name="add_comment"),
    path("", comment_list, name="comment_list"),
    path("<int:comment_id>/", comment_detail, name="comment_detail"),
]

app_name = "comments"
