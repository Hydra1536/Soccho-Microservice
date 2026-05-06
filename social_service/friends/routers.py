from rest_framework.routers import DefaultRouter
from friends.viewsets import FriendshipViewSet

router = DefaultRouter()
router.register(r'friendships', FriendshipViewSet)

urlpatterns = router.urls

