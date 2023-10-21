from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from advertisements.models import Advertisement, AdvertisementFavorite


class UserSerializer(serializers.ModelSerializer):
    """Serializer для пользователя."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name',
                  'last_name',)


class AdvertisementSerializer(serializers.ModelSerializer):
    """Serializer для объявления."""

    creator = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator',
                  'status', 'created_at' )

    def create(self, validated_data):
        """Метод для создания"""

        validated_data["creator"] = self.context["request"].user

        return super().create(validated_data)

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        current_user = self.context["request"].user
        number_open = Advertisement.objects.filter(creator=current_user, status='OPEN').count()
        if number_open >= 10 and data.get('status') not in ['CLOSED', 'DRAFT', None]:
            raise ValidationError("Превышен лимит открытых объявлений (10)")
        return data

class AdvertisementFavoriteSerializer(serializers.ModelSerializer):
    """Serializer для избранного."""
    class Meta:
        model = AdvertisementFavorite
        fields = ('advertisement', 'user' )

    def validate(self, data):
        """Метод для валидации. Вызывается при создании и обновлении."""

        if data['user'] == data['advertisement'].creator:
            raise ValidationError("Вы не можете добавить свое объявление в избранное")
        return data