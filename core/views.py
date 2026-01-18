from django.contrib.auth import authenticate, get_user_model
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

