from .models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

@api_view(['GET', 'POST'])
def signup(request):
    if request.method == 'POST':
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        password = request.data.get('password')
        user = User.objects.create(first_name=first_name, last_name=last_name, email=email, password=password)
        return Response(user.id, status=status.HTTP_201_CREATED)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = User.objects.filter(email=email, password=password).first()
    if user:
        return Response(user.id, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_401_UNAUTHORIZED)



