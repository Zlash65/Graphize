import json

from django.http import QueryDict

from common.logger import tracelog


def read_data_from_request(request):
    '''
        - iterate through all variants of fetching data from request object
    '''

    try:
        if hasattr(request, 'data') and request.data:
            if isinstance(request.data, QueryDict):
                return request.data.dict()
            else:
                return request.data.copy()

        elif hasattr(request, 'body') and request.body:
            try: request_body = request.body.decode()
            except Exception as e: request_body = request.body
            return json.loads(request_body)

        elif hasattr(request, 'POST') and request.POST:
            return request.POST.copy()

        elif hasattr(request, 'GET') and request.GET:
            return request.GET.dict()
        else:
            return dict()

    except Exception as e:
        tracelog("Error reading data from request", repr(e))
        return dict()


def get_json_response_of_api_call(response):
    '''
        - read data from response object
    '''

    try:
        try:
            resp_json = response.json()
        except Exception as e:
            resp_json = json.loads(response.text)
    except Exception as e:
        try:
            resp_json = json.loads(response.content)
        except Exception as e:
            resp_json = dict()

    return resp_json
