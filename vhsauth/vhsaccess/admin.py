from django.contrib import admin
from vhsaccess.models import RawAccessCode
from vhsaccess.models import ScanLog
from vhsaccess.models import AccessCode


class RawAccessCodeAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'email', 'state', 'notes']
    list_display = ('code', 'name', 'email', 'state', 'notes', 'datetime')
    search_fields = ['code', 'name', 'email', 'state', 'notes']
    readonly_fields = ['code', 'name', 'email', 'state', 'notes']

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class AccessCodeAdmin(admin.ModelAdmin):
    fields = ['code', 'name', 'email', 'state', 'notes']
    list_display = ('code', 'name', 'email', 'state', 'notes', 'datetime')
    search_fields = ['code', 'name', 'email', 'state', 'notes']
    list_filter = ['state']
    readonly_fields = ['code']
    ordering = ['-datetime', '-state']

    def has_delete_permission(self, request, obj=None):
        return False


class ScanLogAdmin(admin.ModelAdmin):
    fields = ['code', 'response', 'datetime']
    list_display = ('code', 'response', 'datetime')
    search_fields = ['code', 'response', 'datetime']
    readonly_fields = ['code', 'response', 'datetime']

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(RawAccessCode, RawAccessCodeAdmin)
admin.site.register(ScanLog, ScanLogAdmin)
admin.site.register(AccessCode, AccessCodeAdmin)