from django.shortcuts import render
from rest_framework import viewsets, permissions, pagination, generics, filters
from rest_framework.views import APIView
from .serializers import PostSerializer, TagSerializer, FeedBackSerializer, RegisterSerializer, UserSerializer, CommentSerializer
from .models import Post, Tag, FeedBack, Comment
from rest_framework.response import Response

class PageNumberSetPagination(pagination.PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    ordering = 'created_at'

class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    lookup_field = 'name'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination

# '^' Starts-with search.
# '=' Exact matches.
# '@' Full-text search. (Currently only supported Django's MySQL backend.)
# '$' Regex search.

class PostViewSet(viewsets.ModelViewSet):
    search_fields = ['content', 'h1', 'tags']
    filter_backends = (filters.SearchFilter,)
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'slug'
    permission_classes = [permissions.AllowAny]
    pagination_class = PageNumberSetPagination


class TagDetailView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PageNumberSetPagination
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug'].lower()
        tag = Tag.objects.get(url=slug)
        return Post.objects.filter(tags=tag)

class AsideView(generics.ListAPIView):
    queryset = Post.objects.all().order_by('-id')[:5]
    serializer_class = PostSerializer
    permission_classes = [permissions.AllowAny]

class FeedBackViewSet(viewsets.ModelViewSet):
    queryset = FeedBack.objects.all()
    serializer_class = FeedBackSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        serializer.save(serializer)

        # data = serializer.validated_data
        # name = data.get('name')
        # email = data.get('email')
        # title = data.get('title')
        # message = data.get('message')
        # send_mail(f'От {name} | {subject}', message, 'my email', email)

class RegisterView(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "message": "Пользователь успешно создан",
        })

class ProfileView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request, *args,  **kwargs):
        return Response({
            "user": UserSerializer(request.user, context=self.get_serializer_context()).data,
        })


class CommentView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post_slug = self.kwargs['post_slug'].lower()
        post = Post.objects.get(slug=post_slug)
        return Comment.objects.filter(post=post)


class CommentDeleteView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        username = request.user
        comment_id = self.kwargs.get('comment_id')
        comment = Comment.objects.get(id=comment_id)
        if comment.username == username:
            comment.delete()
            return Response({
                "comment": comment.text,
                "message": "Comment успешно deleted",
            })
        else:
            return Response({
                "message": "User dont have rights for deletion",
            })