from django.http import HttpResponse
from django.http import HttpResponseRedirect
from vhsaccess.models import AccessCode
from vhsaccess.models import ScanLog
from django.core import exceptions


def index(request):
    return HttpResponseRedirect("/admin")


def authorize(request, code):
    isauthorized = False
    try:
        key = AccessCode.objects.get(code=code) # limit new keys to the appropriate size, if they are too long unauthorize
    except exceptions.ObjectDoesNotExist:
        key = None

    if key is not None:
        if key.state == "ACTIVE":
            isauthorized = True
    else:
        newkey = AccessCode(name="", email="", code=code, state="UNREGISTERED")
        newkey.save()

    response = "UNAUTHORIZED"

    if isauthorized:
        response = "AUTHORIZED"

    log = ScanLog(code=code, response=response)
    log.save()

    return HttpResponse(response)