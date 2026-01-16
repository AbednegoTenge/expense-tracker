from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Income, Expense

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        # Set username = email to satisfy Django unique constraint
        validated_data['username'] = validated_data['email']
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.save()
        return user



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)



class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = ['id', 'amount', 'date', 'category', 'description']


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'date', 'category', 'description']

