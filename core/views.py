from django.contrib.auth import authenticate, get_user_model
from django.db.models import Sum
from django.utils.timezone import now
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .serializer import UserSerializer, ExpenseSerializer, IncomeSerializer, LoginSerializer
from .models import Expense, Income

User = get_user_model()


class AuthViewSet(viewsets.ModelViewSet):
    """
    Authentication ViewSet using Django User model
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # Disable default endpoints
    http_method_names = ['post']

    @action(detail=False, methods=['post', 'get'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "user_id": user.id,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED
        )


    @action(detail=False, methods=['get', 'post'], serializer_class=LoginSerializer)
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(username=email, password=password)

        if not user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.id,
                "email": user.email,
            },
            status=status.HTTP_200_OK
        )

    
    @action(detail=False, method=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except Token.DoesNotExist:
            pass

        return Response(
            {'message': 'Logged out successfully'},
            status=status.HTTP_200_OK
            )

    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        user = request.user
        return Response(
            {
                "id": user.id,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }
        )



class ExpenseViewSet(viewsets.ModelViewSet):
    """
    CRUD for Expenses. Each user sees only their own data.
    """
    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only expenses for the logged-in user
        return Expense.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the current user automatically
        serializer.save(user=self.request.user)

    
    @action(detail=False, methods=['get'])
    def monthly_summary(self, request):
        user = request.user

        month = request.query_params.get('month')
        year = request.query_params.get('year')

        today = now()
        month = int(month) if month else today.month
        year = int(year) if year else today.year

        total_expenses = Expense.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        total_income = Income.objects.filter(
            user=user,
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

        return Response(
            {
                "month": month,
                "year": year,
                "total_income": total_income,
                "total_expenses": total_expenses,
                "balance": total_income - total_expenses,
            }
        )



class IncomeViewSet(viewsets.ModelViewSet):
    """
    CRUD for Incomes. Each user sees only their own data.
    """
    serializer_class = IncomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Return only incomes for the logged-in user
        return Income.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Assign the current user automatically
        serializer.save(user=self.request.user)

