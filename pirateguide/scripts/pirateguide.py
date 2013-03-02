#!/usr/bin/env python

import os
import sys
import time
import logging

from optparse import OptionParser

import transaction
import requests
import watchdog

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pyramid.scripts.pserve import PServeCommand
from sqlalchemy import engine_from_config
from sqlalchemy.exc import IntegrityError

from pyramid.paster import (
    get_appsettings,
    setup_logging,
)

from ..models import (
    DBSession,
    Base,
    Movies,
)

from ..lib import filesystem

log = logging.getLogger(__name__)

def initialize_db(settings):
    """ Initialize :app:`pirateguide`s database.

    This only needs to be run once. Though, it can safely be called multiple
    times.
    """

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.create_all(engine)

def find_movies(library, blacklist=None):
    """ Walk the provided ``library`` path and returns a list of paths the
    discovered movie files.
    """

    movies = set([])

    for path in filesystem.filelist(library):
        if not filesystem.is_movie(path) or filesystem.is_sample(path):
            continue

        movies.add(path)

    return movies

class TMDB(object):

    def __init__(self, api_key):
        self.api_key = api_key

    def request(self, request, params=None):
        """ Wrapper for making API requests to The Movie Database.

        See `TMDB <http://docs.themoviedb.apiary.io/>`__ for help on using
        the API.
        """

        if not params:
            params = {}

        params.update({'api_key': self.api_key})

        if request.startswith('/'):
            request = request[1:]

        request  = 'http://api.themoviedb.org/3/{0}'.format(request)
        r        = requests.get(request, params=params)
        response = r.json()

        return response

def add_movie_path(tmdb, path, movie_name):
    """ Downloads the movie information, for the provided ``path``, and
    writes the movie to the database.
    """

    resp = tmdb.request('/search/movie', {
        'query':         movie_name,
        'include_adult': True
    })

    try:
        tmdb_id = resp['results'][0]['id']
    except (KeyError, IndexError):
        log.info('unknown movie: {0}'.format(path))

        movie = Movies(None, path)
    else:
        log.info('adding movie: {0}'.format(path))

        resp = tmdb.request('/movie/{0}'.format(tmdb_id))

        movie            = Movies(tmdb_id, path)
        movie.tmdb_cache = resp

    try:
        with transaction.manager:
            movie.save()
    except IntegrityError:
        log.info('skipping movie: {0}'.format(path))

class LibraryEventHandler(FileSystemEventHandler):

    def __init__(self, tmdb):
        self.tmdb = tmdb

    def on_moved(self, event):
        super(LibraryEventHandler, self).on_created(event)

        if event.is_directory:
            return

        if (filesystem.is_movie(event.dest_path)
            or filesystem.is_sample(event.dest_path)):
            return

        filename   = os.path.basename(event.dest_path)
        movie_name = Movies.clean_filename(filename, blacklist)

        log.info('updating movie: "{0}"'.format(event.dest_path))

        movie      = Movies.by_path(event.src_path)
        movie.path = event.dest_path
        movie.save()

    def on_created(self, event):
        super(LibraryEventHandler, self).on_created(event)

        if event.is_directory:
            return

        if (filesystem.is_movie(event.src_path)
            or filesystem.is_sample(event.src_path)):
            return

        filename   = os.path.basename(event.src_path)
        movie_name = Movies.clean_filename(filename, blacklist)

        log.info('adding new movie: "{0}"'.format(event.src_path))

        add_movie_path(self.tmdb, event.src_path, movie_name)

    def on_deleted(self, event):
        super(LibraryEventHandler, self).on_created(event)

        if event.is_directory:
            return

        movie = Movies.by_path(event.src_path)

        log.info('deleting movie: "{0}"'.format(event.src_path))

        if movie:
            movie.delete()

def main(argv=sys.argv):
    parser = OptionParser(usage='usage: %prog [options] <config_uri>')
    parser.add_option('-i', '--init-db',
                      action='store_true', default=False,
                      help='initialize the database')
    parser.add_option('-s', '--skip-scan',
                      action='store_true', default=False,
                      help='skip directory scan on startup')
    parser.add_option('-w', '--no-watchdog',
                      action='store_true', default=False,
                      help=("disable monitoring of file system events in the "
                            "library"))
    parser.add_option('-n', '--no-daemon',
                      action='store_true', default=False,
                      help="don't daemonize")

    (options, args) = parser.parse_args()

    if len(args) < 1:
        parser.print_usage()
        sys.exit(1)

    setup_logging(args[0])

    settings  = get_appsettings(args[0])
    libraries = settings['movies.directories'].split('\n')
    api_key   = settings['movies.api_key']

    if options.init_db:
        initialize_db(settings)

    if not options.skip_scan:
        with open(settings['movies.blacklist'], 'r') as f:
            blacklist = [i.strip() for i in f]

        tmdb = TMDB(api_key)

        for library in libraries:
            for path in find_movies(library, blacklist):
                filename   = os.path.basename(path)
                movie_name = Movies.clean_filename(filename, blacklist)

                add_movie_path(tmdb, path, movie_name)

    if not options.no_watchdog:
        observer = Observer()

        for library in libraries:
            observer.schedule(LibraryEventHandler(tmdb), library,
                              recursive=True)

        observer.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()

        observer.join()
