from asyncore import poll
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


from . import views


router = routers.DefaultRouter()
# router.register('all', views.SimplePollViewSet, basename='polls')
# router.register('detailed', views.DetailedPollViewSet, basename='polls-detailed' )
router.register('polls', views.DetailedPollViewSet, basename='polls')


# polls/<id>/comments
polls_router = routers.NestedDefaultRouter(router, 'polls', lookup='poll')
polls_router.register('comments', views.CommentViewSet, basename="poll-comments")

urlpatterns = router.urls + polls_router.urls

# urlpatterns = [
#     path('', SimplePollView.as_view()),
#     path('test', RegisterVote.as_view())
# ]