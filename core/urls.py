from rest_framework_nested import routers

from . import views
from pollish.views import PollViewSet, CommentViewSet, CommunityViewSet

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')

# /users/<id>/polls
users_router = routers.NestedDefaultRouter(router, 'users', lookup='user')
users_router.register('polls', PollViewSet, basename='polls')

#/users/<id>/communities
users_router.register('communities', CommunityViewSet, basename='communities')

# /users/<id>/polls/<id>/comments
polls_router = routers.NestedDefaultRouter(users_router, 'polls', lookup='poll')
polls_router.register('comments', CommentViewSet, basename="poll-comments")

urlpatterns = router.urls + users_router.urls + polls_router.urls
