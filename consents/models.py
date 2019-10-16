from datetime import timedelta
from django.conf import settings
from django.contrib.auth.models import Group
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
import uuid


def year_ahead(weeks=52):
    return timezone.now() + timedelta(weeks=weeks)


class DataUseConsentPurpose(models.Model):
    name = models.CharField(max_length=64)
    description_fi = models.TextField()
    description_sv = models.TextField()
    description_en = models.TextField()
    # version = models.IntegerField()  # maybe later

    def __str__(self):
        return self.name


class DataUseConsent(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # granted = models.BooleanField()  # permission active right now?
    issued_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(default=year_ahead)

    # not "issuer" because an admin user can actually create/issue the object on behalf of the user
    consenter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purpose = models.ForeignKey(DataUseConsentPurpose, on_delete=models.CASCADE)
    # permission granted to this group
    audience = models.ForeignKey(Group, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.UUIDField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return "Access to {} allowed for group {} with purpose {}".format(self.content_object, self.audience, self.purpose)
