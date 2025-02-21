from django.contrib import admin
from django.shortcuts import render
from django.urls import path
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.admin import SimpleListFilter
import csv
import io

from clients.models import Client
from .models import ParketUser

class ClientListFilter(SimpleListFilter):
    title = 'client'
    parameter_name = 'client'

    def lookups(self, request, model_admin):
        if request.user.is_superuser:
            return [(c.id, c.name) for c in Client.objects.all()]
        return [(c.id, c.name) for c in request.user.administered_clients.all()]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(client_id=self.value())
        return queryset

class ParketUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'license_plate', 'client')
    list_filter = (ClientListFilter,)
    search_fields = ('first_name', 'last_name', 'email', 'license_plate')

    change_list_template = "admin/parketuser_changelist.html"

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

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-csv/', self.upload_csv, name='upload-csv'),
        ]
        return custom_urls + urls

    def upload_csv(self, request):
        if request.method == "POST":
            csv_file = request.FILES.get("csv_file")
            client_id = request.POST.get("client_id")

            if not csv_file or not client_id:
                self.message_user(request, "Please provide both a CSV file and select a client", level=messages.ERROR)
                return HttpResponseRedirect("../")

            if not csv_file.name.endswith('.csv'):
                self.message_user(request, "Please upload a CSV file", level=messages.ERROR)
                return HttpResponseRedirect("../")

            decoded_file = csv_file.read().decode('utf-8')
            csv_data = csv.reader(io.StringIO(decoded_file))

            # Validate headers
            required_headers = {'first_name', 'last_name', 'email', 'license_plate'}
            headers = {h.lower().strip() for h in next(csv_data)}

            if not required_headers.issubset(headers):
                missing = required_headers - headers
                self.message_user(
                    request,
                    f"Missing required headers: {', '.join(missing)}",
                    level=messages.ERROR
                )
                return HttpResponseRedirect("../")

            # Reset file pointer and use DictReader
            csv_data = csv.DictReader(io.StringIO(decoded_file))
            users_created = 0
            errors = []

            for row in csv_data:
                try:
                    ParketUser.objects.create(
                        first_name=row['first_name'].strip(),
                        last_name=row['last_name'].strip(),
                        email=row['email'].strip(),
                        license_plate=row['license_plate'].strip(),
                        client_id=client_id
                    )
                    users_created += 1
                except Exception as e:
                    errors.append(f"Error on row {users_created + 1}: {str(e)}")

            if errors:
                for error in errors:
                    self.message_user(request, error, level=messages.ERROR)

            self.message_user(
                request,
                f"Successfully created {users_created} users",
                level=messages.SUCCESS if users_created > 0 else messages.WARNING
            )
            return HttpResponseRedirect("../")

        # Get available clients for the current user
        if request.user.is_superuser:
            clients = Client.objects.all()
        else:
            clients = request.user.administered_clients.all()

        context = {
            'clients': clients,
            'has_permission': True,
            'opts': self.model._meta,
        }
        return render(request, "admin/csv_upload.html", context)

admin.site.register(ParketUser, ParketUserAdmin)
