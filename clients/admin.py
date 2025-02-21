from django.contrib import admin
from .models import Client

class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    filter_horizontal = ('administrators',)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(administrators=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return request.user in obj.administrators.all()

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

admin.site.register(Client, ClientAdmin)
