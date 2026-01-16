from rest_framework.routers import DefaultRouter
from .views import ExpenseViewSet, IncomeViewSet, AuthViewSet

router = DefaultRouter()
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'expenses', ExpenseViewSet, basename='expense')
router.register(r'incomes', IncomeViewSet, basename='income')

urlpatterns = router.urls
