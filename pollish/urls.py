from rest_framework_nested import routers


from . import views


router = routers.DefaultRouter()
router.register('polls', views.PollViewSet, basename='polls' )
router.register('profiles', views.ProfileViewSet,  basename='profiles')
router.register('communities', views.CommunityViewSet, basename='communities')


polls_router = routers.NestedDefaultRouter(router, 'polls', lookup='poll')

# polls/<id>/comments
polls_router.register('comments', views.CommentViewSet, basename="comments")

# polls/<id>/images
polls_router.register('images', views.PollImageUpload, basename='images' )

# polls/<id>/choices
# polls_router.register('choices', views.RegisterVote, basename='choices' )

communities_router = routers.NestedDefaultRouter(router, 'communities', lookup='community')

# communities/<id>/polls
communities_router.register('polls', views.PollViewSet, basename='polls')


urlpatterns = router.urls + polls_router.urls + communities_router.urls