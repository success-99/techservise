from rest_framework import serializers
from users.models import CustomUser
from rest_framework.exceptions import ValidationError


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'password', 'password2', 'first_name', 'last_name')
        extra_kwargs = {
            'email': {'required': True},
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2'] or len(attrs['password']) < 4:
            raise serializers.ValidationError({"password": "Password fields didn't match or should have at least 4."})
        return attrs

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = CustomUser.objects.filter(email=email).first()

            if not user:
                msg = 'Foydalanuvchi emaili xato'
                raise ValidationError(msg, code='authorization')
            if not user.check_password(password):
                msg = 'paroli xato'
                raise ValidationError(msg, code='authorization')
        else:
            msg = 'Foydalanuvchi emaili va parolni kiriting'
            raise ValidationError(msg, code='authorization')

        return data
