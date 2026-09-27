from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter

from .views import CommentViewSet, GroupViewSet, PostViewSet

router = SimpleRouter()
router.register('posts', PostViewSet, basename='post')
router.register('groups', GroupViewSet, basename='group')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comment',
)

urlpatterns = [
    path('api-token-auth/', obtain_auth_token, name='api-token-auth'),
    path('', include(router.urls)),
]
