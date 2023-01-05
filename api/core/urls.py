from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, TagViewSet, TagDetailView, AsideView, FeedBackViewSet, RegisterView, ProfileView, CommentView, CommentDeleteView

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('tags', TagViewSet, basename='tags')
router.register('feedback', FeedBackViewSet, basename='feedback')

urlpatterns = [
    path("tags/<slug>/", TagDetailView.as_view(), name="tag"),
    path("aside/", AsideView.as_view()),
    path("", include(router.urls)),
    path('register/', RegisterView.as_view()),
    path('profile/', ProfileView.as_view()),
    path("comments/", CommentView.as_view()),
    path("comments/<post_slug>/", CommentView.as_view()),
    path("comments/delete/<int:comment_id>", CommentDeleteView.as_view()),
]