import logging

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from common.utils import read_data_from_request

log = logging.getLogger(__name__)


@api_view(['POST'])
def create_graphie(request):
    fail_message = {"status": False, "message": ""}
    success_message = {"status": True, "message": "Graphie saved!"}
    try:
        recv_data = read_data_from_request(request)

        if not recv_data.get("grapher_name", None):
            fail_message.update({"message": "Grapher name missing."})
            return JsonResponse(fail_message, status=400)

        if not recv_data.get("username", None):
            fail_message.update({"message": "Please provide a unique identification for the grapher."})
            return JsonResponse(fail_message, status=400)


        return JsonResponse({"status": True, "message": "Graphie saved!"}, status=200)

    except Exception as e:
        tracelog("CREATE STORY ERROR", repr(e))
        return JsonResponse({"status": False, "message": "Encountered an error \
            while saving your story. Please try again."}, status=400)
