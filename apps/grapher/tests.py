import requests

from PIL import Image
import moviepy.editor as mp

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from apps.grapher import views
from common.utils import get_json_response_of_api_call

from Graphize.settings import BASE_DIR
from Graphize.settings import MEDIA_ROOT
from Graphize.settings import TEMP_IMAGE_PATH
from Graphize.settings import TEMP_VIDEO_PATH

class Graphize(TestCase):

    def setUp(self):
        copy_test_low_resolution_image()
        copy_test_high_resolution_image()
        copy_test_low_resolution_video()
        copy_test_high_resolution_video()
        copy_test_random_file()


    def tearDown(self):
        from apps.grapher.models import FileManager
        from common.file_handler import delete_file_from_disk

        filepaths = list(FileManager.objects.all().values_list("filepath", flat=True).all())
        for filepath in filepaths:
            delete_file_from_disk(f"{BASE_DIR}/{filepath}")


    def test_grapher_name_missing(self):
        '''
            - test case to check failure when Grapher name is missing
        '''

        params = {"grapher": "Deku"}
        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Grapher name missing.", True)


    def test_subject_missing(self):
        '''
            - test case to check failure when Story subject is missing
        '''

        params = {"grapher_name": "Deku"}
        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Please provide the name of your story.", True)


    def test_description_missing(self):
        '''
            - test case to check failure when Story description is missing
        '''

        params = {"grapher_name": "Deku", "subject": "Infinte 100%"}
        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Please add a description for your story.", True)


    def test_graphie_missing(self):
        '''
            - test case to check failure when Story illustration file is missing
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Please upload the appropriate file your story.", True)


    def test_longitude_missing(self):
        '''
            - test case to check failure when latitude is given and longitude is missing
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "description": "Exceeding body limit and unlocking 100% of One for All.", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg"}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Please provide a valid longitude for the given latitude.", True)


    def test_latitude_missing(self):
        '''
            - test case for to check failure when longitude is given and latitude is missing
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All.", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg"}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Please provide a valid latitude for the given longitude.", True)


    def test_latitude_wrong_value(self):
        '''
            - test case to check failure when invalid latitude value is provided
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685X", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Invalid value for Latitude.", True)


    def test_longitude_wrong_value(self):
        '''
            - test case to check failure when invalid longitude value is provided
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg", "longitude": "72.902334X", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Invalid value for Longitude.", True)


    def test_wrong_file_input(self):
        '''
            - test case to check failure when non image/video file is uploaded
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_IMAGE_PATH}/req.txt", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Uploaded file is not an image / video", True)


    def test_create_graphie_success(self):
        '''
            - test case to check successful story posting
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["message"] == "Graphie saved!", True)


    def test_check_no_resize_for_low_resolution_image(self):
        '''
            - test case to check no resizing for already lower resolution image
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        from apps.grapher.models import Graphie
        graphie = Graphie.objects.last()

        im = Image.open(f"{TEMP_IMAGE_PATH}/test-low-resolution.jpeg")
        original_width, original_height = im.size

        im = Image.open(f"{BASE_DIR}/{graphie.illustration.filepath}")
        new_width, new_height = im.size

        self.assertEqual(original_width == new_width, True)
        self.assertEqual(original_height == new_height, True)


    def test_check_no_resize_for_low_resolution_video(self):
        '''
            - test case to check no resizing for already lower resolution video
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_VIDEO_PATH}/test-low-resolution.mp4", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        from apps.grapher.models import Graphie
        graphie = Graphie.objects.last()

        clip = mp.VideoFileClip(f"{TEMP_VIDEO_PATH}/test-low-resolution.mp4")
        original_width, original_height = clip.size[0], clip.size[1]

        clip = mp.VideoFileClip(f"{BASE_DIR}/{graphie.illustration.filepath}")
        new_width, new_height = clip.size[0], clip.size[1]

        self.assertEqual(original_width == new_width, True)
        self.assertEqual(original_height == new_height, True)


    def test_check_resize_for_high_resolution_image(self):
        '''
            - test case to check resizing for high resolution image - downscale resolution
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_IMAGE_PATH}/test-high-resolution.jpg", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        from apps.grapher.models import Graphie
        graphie = Graphie.objects.last()

        im = Image.open(f"{TEMP_IMAGE_PATH}/test-high-resolution.jpg")
        original_width, original_height = im.size

        im = Image.open(f"{BASE_DIR}/{graphie.illustration.filepath}")
        new_width, new_height = im.size
        print(new_width, new_height)

        # asset for changed values
        self.assertEqual(original_width != new_width, True)
        self.assertEqual(original_height != new_height, True)

        # assert for original values will be greater or equal to new
        self.assertEqual(original_width >= new_width, True)
        self.assertEqual(original_height >= new_height, True)


    def test_check_resize_for_high_resolution_video(self):
        '''
            - test case to check resizing for high resolution video - downscale resolution
        '''

        params = {"grapher_name": "Test", "subject": "Infinte 100%", "latitude": "20.938685", \
            "graphie": f"{TEMP_VIDEO_PATH}/test-high-resolution.mp4", "longitude": "72.902334", \
            "description": "Exceeding body limit and unlocking 100% of One for All."}

        factory = APIRequestFactory()
        request = factory.post('/create-graphie/', params, format="json")
        request.test_runner = True

        response = views.create_graphie(request)
        response = get_json_response_of_api_call(response)

        from apps.grapher.models import Graphie
        graphie = Graphie.objects.last()

        clip = mp.VideoFileClip(f"{TEMP_VIDEO_PATH}/test-high-resolution.mp4")
        original_width, original_height = clip.size[0], clip.size[1]

        clip = mp.VideoFileClip(f"{BASE_DIR}/{graphie.illustration.filepath}")
        new_width, new_height = clip.size[0], clip.size[1]
        print(new_width, new_height)

        # asset for changed values
        self.assertEqual(original_width != new_width, True)
        self.assertEqual(original_height != new_height, True)

        # assert for original values will be greater or equal to new
        self.assertEqual(original_width >= new_width, True)
        self.assertEqual(original_height >= new_height, True)


    def test_get_graphie_list(self):
        '''
            - test case to check fetching stories API
        '''

        factory = APIRequestFactory()
        request = factory.post('/get-graphie-list/', {"test": True}, format="json")
        request.test_runner = True

        response = views.get_graphie_list(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["status"], True)


    def test_get_graphie_list_for_valid_grapher(self):
        '''
            - test case to check fetching stories for a valid grapher
        '''

        self.test_create_graphie_success()
        factory = APIRequestFactory()
        request = factory.post('/get-graphie-list/', {"test": True}, format="json")
        request.test_runner = True

        response = views.get_graphie_list(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(len(response["graphies"]) > 0, True)


    def test_get_graphie_list_for_invalid_grapher(self):
        '''
            - test case to check fetching stories for an invalid grapher
        '''

        self.test_create_graphie_success()
        params = {"grapher_name": "Midoriya Izuku"}

        factory = APIRequestFactory()
        request = factory.post('/get-graphie-list/', params, format="json")
        request.test_runner = True

        response = views.get_graphie_list(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(len(response["graphies"]) == 0, True)


    def test_get_graphie_list_for_radius_success(self):
        '''
            - test case to check fetching stories in a given radius from a location - success
        '''

        self.test_create_graphie_success()
        params = {"latitude": "20.941229", "longitude": "72.901467"}

        factory = APIRequestFactory()
        request = factory.post('/get-graphie-list/', params, format="json")
        request.test_runner = True

        response = views.get_graphie_list(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(len(response["graphies"]) > 0, True)


    def test_get_graphie_list_for_radius_failure(self):
        '''
            - test case to check fetching stories in a given radius from a location - failure
        '''

        self.test_create_graphie_success()
        params = {"latitude": "20.941229", "longitude": "72.901467", "radius": 20}

        factory = APIRequestFactory()
        request = factory.post('/get-graphie-list/', params, format="json")
        request.test_runner = True

        response = views.get_graphie_list(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(len(response["graphies"]) == 0, True)


    def test_get_graphie_illustration(self):
        '''
            - test case to check fetching illustration file for the story
        '''

        self.test_create_graphie_success()
        from apps.grapher.models import Graphie
        graphie = Graphie.objects.last()
        params = {"uuid": graphie.uu}

        factory = APIRequestFactory()
        request = factory.post('/get-graphie-illustration/', params, format="json")
        request.test_runner = True

        response = views.get_graphie_illustration(request)
        response = get_json_response_of_api_call(response)

        self.assertEqual(response["status"], True)


def copy_test_low_resolution_image():
    filename = "test-low-resolution.jpeg"

    with open(f"{MEDIA_ROOT}/images/{filename}", "rb") as file_reader:
        file_content = file_reader.read()
    with open(f"{TEMP_IMAGE_PATH}/{filename}", "wb") as file_writer:
        file_writer.write(file_content)


def copy_test_high_resolution_image():
    filename = "test-high-resolution.jpg"

    with open(f"{MEDIA_ROOT}/images/{filename}", "rb") as file_reader:
        file_content = file_reader.read()
    with open(f"{TEMP_IMAGE_PATH}/{filename}", "wb") as file_writer:
        file_writer.write(file_content)


def copy_test_low_resolution_video():
    filename = "test-low-resolution.mp4"

    with open(f"{MEDIA_ROOT}/videos/{filename}", "rb") as file_reader:
        file_content = file_reader.read()
    with open(f"{TEMP_VIDEO_PATH}/{filename}", "wb") as file_writer:
        file_writer.write(file_content)


def copy_test_high_resolution_video():
    filename = "test-high-resolution.mp4"

    with open(f"{MEDIA_ROOT}/videos/{filename}", "rb") as file_reader:
        file_content = file_reader.read()
    with open(f"{TEMP_VIDEO_PATH}/{filename}", "wb") as file_writer:
        file_writer.write(file_content)


def copy_test_random_file():
    filename = "req.txt"

    with open(f"{BASE_DIR}/{filename}", "rb") as file_reader:
        file_content = file_reader.read()
    with open(f"{TEMP_IMAGE_PATH}/{filename}", "wb") as file_writer:
        file_writer.write(file_content)
