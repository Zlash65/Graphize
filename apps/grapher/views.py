import os
import magic
import logging
import filetype
from decimal import Decimal

from django.db.models import F, Q
from django.http import JsonResponse
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from rest_framework.decorators import api_view
from rest_framework.response import Response

from apps.grapher.models import Grapher, Graphie, FileManager
from apps.grapher.helpers import validate_information
from apps.grapher.helpers import validate_location_info

from common.logger import tracelog
from common.utils import read_data_from_request
from common.file_handler import get_content_hash

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

        file_content = recv_data["graphie"].read()
        mimetype_info = filetype.guess(file_content)
        if "image" not in mimetype_info.mime and "video" not in mimetype_info.mime:
            fail_message.update({"message": "Uploaded file is not an image / video"})
            return JsonResponse(fail_message, status=400)
        else:
            recv_data["file_extension"] = mimetype_info.extension
            recv_data["file_type"] = "1" if "image" in mimetype_info.mime else "2"

        status, graphie = Graphie.add_graphie(recv_data)
        if not status:
            fail_message.update({"message": "Encountered an error while saving your Story."})
            return JsonResponse(fail_message, status=400)

        # store file in temporary location for further processing
        status = FileManager.add_file(recv_data, graphie=graphie, file_content=file_content)
        if not status:
            Graphie.objects.filter(uu=graphie.uu).delete()
            fail_message.update({"message": "Please check the uploaded file."})
            return JsonResponse(fail_message, status=400)

        return JsonResponse(success_message, status=200)

    except Exception as e:
        tracelog("CREATE STORY ERROR", repr(e))
        return JsonResponse({"status": False, "message": "Encountered an error " \
            "while saving your Story. Please try again."}, status=400)


@api_view(['POST'])
def get_graphie_list(request):
    '''
        - get list of all stories from latest to oldest
        - condition
            - pass name of Grapher to fetch only their entries
            - pass Latitude and Longitude and the radius to fetch
                all stories in that radius from the location.
            - default radius will be 5000 meters
        - parameter types
            - grapher_name     -> string
            - latitude         -> decimal
            - longitude        -> decimal
            - radius           -> integer (value considered in meters)
    '''

    try:
        condition = dict()
        recv_data = read_data_from_request(request)

        # Formulate condition based on grapher name if provided
        if recv_data.get("grapher_name", ""):
            condition["grapher__name"] = recv_data["grapher_name"]
        if recv_data.get("username", ""):
            username = recv_data["username"]
            condition["grapher__username"] = username

        # Formulate condition based on latitude, longitude if provided
        status, message = validate_location_info(recv_data, exists=True)
        if status :
            radius = int(recv_data.get("radius", 5000))
            latitude = Decimal(recv_data["latitude"])
            longitude = Decimal(recv_data["longitude"])
            condition["location__distance_lt"] = (
                Point([latitude, longitude]),
                Distance(m=radius)
            )

        graphies = list(Graphie.objects.filter(**condition)\
            .annotate(grapher_name=F("grapher__name"))
            .annotate(uuid=F("uu"))
            .order_by("-created_at")
            .values("grapher_name", "subject", "description", "uuid")
        )

        return JsonResponse({"status": True, "graphies": graphies}, status=200)

    except Exception as e:
        tracelog("GET GRAPHIE LIST ERROR", repr(e))
        return JsonResponse({"status": False, "message": "Error fetching stories. " \
            "Please try again in some time."}, status=400)


@api_view(['POST'])
def get_graphie_illustration(request):
    '''
        - pass the uuid of the graphie to fetch its image or video
    '''
    try:
        recv_data = read_data_from_request(request)
        if not recv_data.get("uuid", None):
            return JsonResponse({"status": False, "message": "Please provide a " \
                "valid uuid to fetch the iilustration file."}, status=400)

        # check if the uuid is valid or not
        graphie = Graphie.objects.filter(uu=recv_data["uuid"]).last()
        if not graphie:
            return JsonResponse({"status": False, "message": "Invalid uuid"}, status=400)

        # check if file optimization is completed
        if graphie.status == '1':
            return JsonResponse({"status": False, "message": "Illustration is being " \
                "processed at the moment. Please try again in some time."}, status=400)

        return JsonResponse({"status": True, "filepath": graphie.illustration.filepath})

    except Exception as e:
        tracelog("GET GRAPHIE ILLUSTRATION ERROR", repr(e))
        return JsonResponse({"status": False, "message": "Encountered an error " \
            "while fetching illustration file."}, status=400)
