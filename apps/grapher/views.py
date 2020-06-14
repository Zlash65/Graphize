import logging

from django.http import JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.grapher.models import Grapher, Graphie
from apps.grapher.helpers import validate_information

from common.logger import tracelog
from common.utils import read_data_from_request

log = logging.getLogger(__name__)


@api_view(['POST'])
def create_graphie(request):
    fail_message = {"status": False, "message": ""}
    success_message = {"status": True, "message": "Graphie saved!"}
    try:
        recv_data = read_data_from_request(request)

        status, message = validate_information(recv_data)
        if not status:
            fail_message.update({"message": message})
            return JsonResponse(fail_message, status=400)

        status, graphie = Graphie.add_graphie(recv_data)
        if not status:
            fail_message.update({"message": "Encountered an error while saving your Story."})
            return JsonResponse(fail_message, status=400)

        return JsonResponse(success_message, status=200)

    except Exception as e:
        tracelog("CREATE STORY ERROR", repr(e))
        return JsonResponse({"status": False, "message": "Encountered an error \
            while saving your Story. Please try again."}, status=400)
