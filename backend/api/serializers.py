from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Song, Score
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import bleach

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]
        extra_kwargs = {"password": {"write_only": True}}
        

    def validate_username(self, value):
        return bleach.clean(value)
    def validate_email(self, value):
        return bleach.clean(value)
    def validate_password(self, value):
        return bleach.clean(value)

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data["email"]
        )
        return user
    
class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'
    
class ScoreSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = Score
        fields = ('id', 'score', 'username')

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token_serializer(cls, user):
        token = super().get_token(user)
        # ADD GROUP
        token['groups'] = [group.name for group in user.groups.all()]
        return token