import os
import mimetypes

def filelist(directory):
    """ Recursively walks the provided ``directory`` and returns a list of
    all discovered files.
    """

    files = []

    for dirname, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            path = os.path.join(dirname, filename)

            files.append(path)

    return files

def is_movie(path):
    """ Determins if the file at the given ``path`` is a movie. """

    mimetypes.init()

    mimetype = mimetypes.guess_type(path)[0]

    if not mimetype:
        return False

    if 'video' not in mimetype:
        return False

    return True

def is_sample(path, min_size=40):
    """ Determins if the file at the given ``path`` is a sample.

    Samples are the ~5 minute videos you'll often get in torrents to demo
    the rip quality.
    """

    if os.stat(path).st_size <= min_size * (1024 * 2):
        return True

    return False
