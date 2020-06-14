import os
import six
import hashlib


def get_content_hash(content):
    '''
        - return a hexdigest for file content
    '''
    if isinstance(content, six.string_types):
        content = content.encode('utf-8')

    return hashlib.md5(content).hexdigest()


def get_size_of_file(url):
    '''
        - return the file size
    '''
    return os.path.getsize(url)


def delete_file_from_disk(url):
    os.remove(url)
