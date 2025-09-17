from rest_framework import serializers
from The_Builder.models import Users
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    user_password = serializers.CharField(write_only=True)

    class Meta:
        model = Users
        fields = ['user_id', 'user_full_name', 'user_username', 'user_email', 'user_phone', 'user_password', 'user_type', 'user_is_active', 'created_at', 'updated_at']
        read_only_fields = ['user_id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # yaha aap password ko plain text save kar rahe ho, 
         # check mobile number duplicate
        if Users.objects.filter(user_phone=validated_data.get("user_phone")).exists():
            raise serializers.ValidationError({"user_phone": "This mobile number is already registered."})

        # check email duplicate
        if Users.objects.filter(user_email=validated_data.get("user_email")).exists():
            raise serializers.ValidationError({"user_email": "This email is already registered."})

        # agar hashing chahiye to yaha implement karna hoga
        validated_data['user_password'] = make_password(validated_data['user_password'])  # hash password
        return Users.objects.create(**validated_data)


class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    user_password = serializers.CharField(write_only=True)