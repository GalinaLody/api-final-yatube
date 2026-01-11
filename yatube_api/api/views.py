from django.shortcuts import get_object_or_404
from rest_framework import filters
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAuthorOrReadOnlyPermission
from .serializers import (
    PostSerializer,
    GroupSerializer,
    CommentSerializer,
    FollowSerializer
)
from posts.models import Post, Group, Comment


class ListCreateViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    """Собственный базовый класс.

    Возвращвет список объектов для обработки GET-запроса.
    Создает объект для обработки POST-запроса.
    """


class PostViewSet(viewsets.ModelViewSet):
    """API для работы с публикациями.

    Для работы с частью API требуется аутентификация.
    list:Получить список постов(чтение для всех пользователей).
    retrieve:Получить один пост по id(чтение для всех пользователей).
    create:Создать новый пост(только для аутентифицированных пользователей).
    update:Обновить пост (только автор публикации).
    destroy:Удалить пост (только автор публикации).
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Автоматическое проставление автора.
        При создании публикации в качетсве автора сохраняется
        пользователь, создающий публикацию."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """API для работы с группой публикаций.

    Для работы с API не требуется аутентификация.
    Работает только с GET-запросами.
    list:Получить список групп.
    retrieve:Получить информацию о группе с идентификатором.

    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """API для работы со списком комментарий.

    Для работы с частью API требуется аутентификация.
    list:Получить список комментарий к посту(чтение для всех пользователей).
    create:Создать новый комментарий(только аутентифицированные пользователи).
    retrieve:Получить один комментарий по id(чтение для всех пользователей).
    update:Обновить комментарий (только автор комментария).
    destroy:Удалить комментарий (только автор комментария).
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnlyPermission,)
    lookup_field = 'id'

    def get_post(self):
        """Метод получает объект модели Post на основании id из запроса."""
        return get_object_or_404(Post, id=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        """Автоматическое проставление автора и привязка к публикации.
        При создании комментария в качетсве автора сохраняется
        пользователь, создающий комментарий. Комментарий привязывается
        к объекту, модели Post, указанному в запросе."""
        serializer.save(
            post=self.get_post(),
            author=self.request.user
        )


class FollowViewSet(ListCreateViewSet):
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    permission_classes = (IsAuthenticated,)
    search_fields = ('following__username',)

    def get_queryset(self):
        return self.request.user.follower.all()

    def perform_create(self, serializer):
        """Подписка создается от имени пользователя, сделавшего запрос."""
        serializer.save(
            user=self.request.user
        )
