import uuid
from django.db import models


def make_uuid():
    return str(uuid.uuid1().int >> 64)


class RawAccessCode(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)
    code = models.CharField(max_length=16)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=256)
    state = models.CharField(max_length=16, choices=[
        ('UNREGISTERED', 'UNREGISTERED'),
        ('ACTIVE', 'ACTIVE'),
        ('SUSPENDED', 'SUSPENDED'),
        ('DISABLED', 'DISABLED'),
        ('BLACKLISTED', 'BLACKLISTED'),
    ])
    notes = models.CharField(max_length=1024)
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.uuid = make_uuid()
        #self.datetime = datetime.datetime.now()
        super(RawAccessCode, self).save(force_insert=True)


class AccessCodeManager(models.Manager):
    def get_queryset(self):
        return super(AccessCodeManager, self).get_queryset()\
            .extra(where=["uuid in (select uuid from (select * from (select * from vhsaccess_rawaccesscode order by datetime asc) as x group by code) as s)"])
    pass


class AccessCode(RawAccessCode):
    default_manager = AccessCodeManager()
    objects = AccessCodeManager()

    class Meta:
        proxy = True


class ScanLog(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True, default=make_uuid, editable=False)
    code = models.CharField(max_length=16)
    response = models.CharField(max_length=16)
    datetime = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.uuid = make_uuid()
        #self.datetime = datetime.datetime.now()
        super(ScanLog, self).save(force_insert=True)

