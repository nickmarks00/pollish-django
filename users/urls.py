from django.urls import path, include
from rest_framework_nested import routers

from . import views
from polls.views import DetailedPollViewSet, CommentViewSet

router = routers.DefaultRouter()
router.register('users', views.UserViewSet, basename='users')
router.register('profiles', views.ProfileViewSet,  basename='profiles')


# /users/<id>/polls
users_router = routers.NestedDefaultRouter(router, 'users', lookup='user')
users_router.register('polls', DetailedPollViewSet, basename='polls')

# /users/<id>/polls/<id>/comments
polls_router = routers.NestedDefaultRouter(users_router, 'polls', lookup='poll')
polls_router.register('comments', CommentViewSet, basename="poll-comments")

urlpatterns = router.urls + users_router.urls + polls_router.urls
