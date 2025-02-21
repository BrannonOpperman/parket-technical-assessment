from django.contrib import admin
from .models import ParketUser

class ParketUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'license_plate', 'client')
    list_filter = ('client',)
    search_fields = ('first_name', 'last_name', 'email', 'license_plate')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(client__administrators=request.user)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "client" and not request.user.is_superuser:
            kwargs["queryset"] = request.user.administered_clients.all()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            return True
        return request.user in obj.client.administrators.all()

    def has_delete_permission(self, request, obj=None):
        return self.has_change_permission(request, obj)

admin.site.register(ParketUser, ParketUserAdmin)
