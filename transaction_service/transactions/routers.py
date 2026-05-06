from rest_framework.routers import DefaultRouter
from transactions.viewsets import TransactionViewSet

router = DefaultRouter()
router.register(r'transactions', TransactionViewSet)

urlpatterns = router.urls

