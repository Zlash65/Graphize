import os
import six
import hashlib

from PIL import Image
import moviepy.editor as mp


def get_content_hash(content):
    '''
        - return a hexdigest for file content
    '''
    if isinstance(content, six.string_types):
        content = content.encode('utf-8')

    return hashlib.md5(content).hexdigest()


def get_size_of_file(filepath):
    '''
        - return the file size
    '''
    return os.path.getsize(filepath)


def delete_file_from_disk(filepath):
    os.remove(filepath)


def process_image_file(current_path, final_path):
    '''
        - read the file from temporary path
        - execute downscaling on the image file
        - store the new file to a media path for easy retrieving
    '''

    im = Image.open(current_path)
    width, height = im.size

    if width > 600:
        width = 600

    if height > 1200:
        height = 1200

    resize_to = (height, width)
    resized_image = im.resize(resize_to, Image.ANTIALIAS)
    resized_image.save(f"{final_path}", quality=95)


def process_video_file(current_path, final_path):
    '''
        - read the file from temporary path
        - execute downscaling on the video file
        - store the new file to a media path for easy retrieving
    '''

    clip = mp.VideoFileClip(f"{current_path}")

    original_width, original_height = clip.size[0], clip.size[1]

    if original_height > 480 and original_width > 640:
        clip_resized = clip.resize(height=480, width=640)
        clip_resized.write_videofile(f"{final_path}")

    elif original_height > 480:
        clip_resized = clip.resize(height=480, width=original_width)
        clip_resized.write_videofile(f"{final_path}")

    elif original_width > 640:
        clip_resized = clip.resize(height=original_height, width=640)
        clip_resized.write_videofile(f"{final_path}")

    else:
        with open(current_path, 'rb') as file_writer:
            file_content = file_writer.read()

        with open(final_path, 'wb') as file_writer:
            file_writer.write(file_content)
