from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement, AdvertisementFavorite
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer, AdvertisementFavoriteSerializer
from django.db.models import Q


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filterset_class = AdvertisementFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            queryset = Advertisement.objects.exclude(status='DRAFT')
        else:
            queryset = Advertisement.objects.filter(Q(status='OPEN') | Q(status='CLOSED') | Q(status='DRAFT', creator=self.request.user))
        return queryset
    def get_permissions(self):
        """Получение прав для действий."""

        if self.action in ["create", "update", "partial_update", "destroy"]:
            if self.request.user.is_staff:
                return [IsAuthenticated()]
            else:
                return [IsAuthenticated(), IsOwner()]
        return []

    @action(methods=['post'], detail=False)
    def favorites(self, request):
        """Добавление в избранное."""


        data = {
            'advertisement': request.data.get('advertisement'),
            'user': self.request.user.id
        }

        if AdvertisementFavorite.objects.filter(advertisement=data['advertisement'], user=data['user']):
            return Response('Такое объявление уже есть в избранном')
        else:
            serializer = AdvertisementFavoriteSerializer(data=data)

            if serializer.is_valid():
                serializer.save()
                return Response('Объявление добавлено в избранное')
            return Response('Объявление не добавлено в избранное')


    @action(methods=['delete'], detail=False)
    def favorites_delete(self, request):
        """Удаление из избранного."""

        data = {
            'advertisement': request.data.get('advertisement'),
            'user': self.request.user.id
        }
        if AdvertisementFavorite.objects.filter(advertisement=data['advertisement'], user=data['user']):
            AdvertisementFavorite.objects.get(advertisement=data['advertisement'], user=data['user']).delete()
            return Response('Объявление удалено из избранного')
        return Response('Объявление не удалено из избранного')

    @action(detail=False)
    def favorites_get(self, request):
        """Просмотр избранного."""

        data = AdvertisementFavorite.objects.filter(user=request.user.id)
        serializer = AdvertisementFavoriteSerializer(data, many=True)
        return Response(serializer.data)