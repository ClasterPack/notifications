from django.contrib import admin

from distribution.models import Client, Distribution, Messages


@admin.register(Distribution)
class DistributionModelAdmin(admin.ModelAdmin):
    model = Distribution
    fields = (
        'id',
        'start_time', 'end_time',
        'filter_tag', 'filter_operator_code',
        'message',
    )

    def has_change_permission(self, request, obj=None):
        return False

    search_fields = (
        'id',
        'start_time', 'end_time',
        'filter_tag', 'filter_operator_code',
        'message',
    )
    ordering = ('-start_time',)
    list_display = (
        'id',
        'start_time', 'end_time',
        'filter_tag', 'filter_operator_code',
        'message',
    )
    readonly_fields = ('id', )


@admin.register(Messages)
class MessagesModelAdmin(admin.ModelAdmin):
    model = Messages
    fields = (
        'status', 'client_id',
        'distribution_id',
    )
    search_fields = (
        'id', 'status',
        'timestamp', 'client_id',
        'distribution_id',
    )
    ordering = ('-id',)
    list_display = (
        'id', 'status',
        'timestamp', 'client_id',
        'distribution_id',
    )


@admin.register(Client)
class ClientModelAdmin(admin.ModelAdmin):
    model = Client
    fields = (
        'phone_number', 'operator_code',
        'timezone', 'tag',
    )
    search_fields = (
        'id', 'phone_number', 'operator_code',
        'timezone', 'tag',
    )
    ordering = ('-id',)
    list_display = (
        'id', 'phone_number', 'operator_code',
        'timezone', 'tag',
    )
