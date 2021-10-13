from django.http import JsonResponse, HttpResponseBadRequest
import json


def generate_error(message):
    return HttpResponseBadRequest(message)


def generate_success(data={}):
    return_json = {}

    if type(data) == str:
        return_json.update({"message": data})

    else:
        return_json.update(data)

    return JsonResponse(return_json)


def get_data(request):
    try:
        data = json.loads(request.body.decode())

    except:
        data = {}

    try:
        data["username"] = request.headers["username"]
    except:
        if not "username" in data:
            data["username"] = None

    try:
        data["password"] = request.headers["password"]

    except:
        if not "password" in data:
            data["password"] = None

    return data
