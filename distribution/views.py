from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from distribution.models import Client, Distribution, Messages
from distribution.serializers import (ClientSerializer, DistributionSerializer,
                                      MessageSerializer)


class ClientViewSet(viewsets.ModelViewSet):
    """View set для клиента."""

    serializer_class = ClientSerializer
    queryset = Client.objects.get_queryset().order_by('id')


class MessageViewSet(viewsets.ModelViewSet):
    """View set для сущности сообщений."""

    serializer_class = MessageSerializer
    queryset = Messages.objects.get_queryset().order_by('id')


class DistributionViewSet(viewsets.ModelViewSet):
    """View set для модели рассылок."""

    serializer_class = DistributionSerializer
    queryset = Distribution.objects.get_queryset().order_by('id')

    @action(detail=True, methods=['get'])
    def info(self, request, pk):
        """Общая информация для определенной рассылки."""
        queryset_distribution = Distribution.objects.filter(id=pk)
        get_object_or_404(queryset_distribution, pk=pk)
        mesages = Messages.objects.filter(distribution_id=pk).all()

        result = {
            'Всего сообщений': len(mesages),
            'Сообщений отправленно': mesages.filter(status='sent').count(),
            'Сообщений отменено': mesages.filter(status='canceled').count(),
            'Сообщения в ожидании отправления': mesages.filter(status='pending').count(),
            'Distribution': queryset_distribution.values(),
            'Messages': MessageSerializer(mesages, many=True).data,

        }
        return Response(result)

    @action(detail=False, methods=['get'])
    def full_info(self, request):
        """Общая информация для всех рассылок."""
        total_count = Distribution.objects.count()
        distribution = Distribution.objects.values('id')

        content = {
            'Общее число рассылок': total_count,
        }
        result = {}

        for row in distribution:
            res = {
                'Всего сообщений': 0,
                'Отправленно': 0,
                'Не отправленно': 0,
                'В ожидании отправления': 0,
            }
            msg = Messages.objects.filter(distribution_id=row['id']).all()
            group_sent = msg.filter(status='sent').count()
            group_not_sent = msg.filter(status='not_sent').count()
            group_cancelled = msg.filter(status='cancelled').count()
            group_pending = msg.filter(status='pending').count()
            res['Всего сообщений'] = len(msg)
            res['Отправленно'] = group_sent
            res['Не отправленно'] = group_not_sent
            res['Отменено'] = group_cancelled
            res['В ожидании отправления'] = group_pending
            result[row['id']] = res

        content['Количество сообщений отправленно'] = result
        return Response(content)

    def update(self, request, pk=None):
        """Функция запрещающая обновление модели."""
        response = {'message': 'Невозможно редактировать рассылку.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)

    def partial_update(self, request, pk=None):
        """Функция запрещающая чамтичное обновление модели."""
        response = {'message': 'Невозможно частично менять рассылку.'}
        return Response(response, status=status.HTTP_403_FORBIDDEN)
