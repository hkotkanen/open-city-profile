from django.contrib import admin

from .models import DataUseConsent, DataUseConsentPurpose


@admin.register(DataUseConsent)
class DataUseConsentAdmin(admin.ModelAdmin):
    model = DataUseConsent


@admin.register(DataUseConsentPurpose)
class DataUseConsentPurposeAdmin(admin.ModelAdmin):
    model = DataUseConsentPurpose
