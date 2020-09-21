import os
import uuid
from secrets import token_urlsafe


def generate_token(length=7):
    return token_urlsafe(length)


def get_file_path(instance, filename):
    """
    Rename images
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.__class__.__name__.lower(), filename)
