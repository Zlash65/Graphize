import logging
from decimal import Decimal

log = logging.getLogger(__name__)


def is_none_value(value):
    ''' parse falsify values '''
    if value in [None, False]:
        return False
    else: return True


def validate_location_info(recv_data, exists=False):
    '''
        - check if latitude and longitude data is correct
        - return status and message accordingly
    '''
    status, message = True, ""
    recv_data_keys = recv_data.keys()


    if "latitude" in recv_data_keys and not "longitude" in recv_data_keys:
        status, message = False, "Please provide a valid longitude for the given latitude."
    elif "longitude" in recv_data_keys and not "latitude" in recv_data_keys:
        status, message = False, "Please provide a valid latitude for the given longitude."
    elif "latitude" in recv_data_keys and "longitude" in recv_data_keys:
        try:
            Decimal(recv_data["latitude"])
        except Exception as e:
            status, message = False, "Invalid value for Latitude."

        try:
            if status:
                Decimal(recv_data["longitude"])
            else: pass
        except Exception as e:
            status, message = False, "Invalid value for Longitude."
    else:
        if exists: status, message = False, "No location info provided"

    return status, message


def validate_information(recv_data):
    '''
        - check if all the required data has been posted
    '''
    status, message = True, ""

    if not recv_data.get("grapher_name", None):
        status, message = False, "Grapher name missing."

    # elif not recv_data.get("username", None):
    #     status, message = False, "Please provide a unique username for the grapher."

    elif not recv_data.get("subject", None):
        status, message = False, "Please provide the name of your story."

    elif not recv_data.get("description", None):
        status, message = False, "Please add a description for your story."

    elif not recv_data.get("graphie", None):
        status, message = False, "Please upload the appropriate file your story."

    if status:
        status, message = validate_location_info(recv_data)

    return status, message
