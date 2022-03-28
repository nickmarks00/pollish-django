from asyncore import poll
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers


from . import views


router = routers.DefaultRouter()
router.register('polls', views.PollViewSet, basename='polls' )
router.register('profiles', views.ProfileViewSet,  basename='profiles')


polls_router = routers.NestedDefaultRouter(router, 'polls', lookup='poll')

# polls/<id>/comments
polls_router.register('comments', views.CommentViewSet, basename="comments")

# polls/<id>/images
polls_router.register('images', views.PollImageUpload, basename='images' )

urlpatterns = router.urls + polls_router.urls