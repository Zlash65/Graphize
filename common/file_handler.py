import six
import hashlib


def get_content_hash(content):
    ''' return a hexdigest for file content '''

    if isinstance(content, six.string_types):
        content = content.encode('utf-8')

    return hashlib.md5(content).hexdigest()
