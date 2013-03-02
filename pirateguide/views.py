import subprocess
import shlex

from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import (
    HTTPAccepted,
    HTTPNotFound,
    HTTPNotImplemented,
    HTTPBadRequest,
)

from mako.exceptions import TopLevelLookupException

from .models import (
    DBSession,
    Movies,
)

@view_config(route_name='home', renderer='index.mako')
def home(request):
    if 'movies.streamer' in request.registry.settings:
        stream = True
    else:
        stream = False

    settings = {
        'api_key': request.registry.settings['movies.api_key'],
        'stream':  stream,
    }

    return {'settings': settings}

@view_config(route_name='partials')
def partials(request):
    partial = request.matchdict['partial']
    path    = 'pirateguide:templates/{0}.mako'.format(partial)

    try:
        return render_to_response(path, {}, request=request)
    except TopLevelLookupException:
        return HTTPNotFound()

@view_config(route_name='movie.list', renderer='json')
def movie_list(request):
    return Movies.all()

@view_config(route_name='movie.stream', request_method='POST', renderer='json')
def stream(request):
    try:
        streamer = request.registry.settings['movies.streamer']
    except KeyError:
        return HTTPNotImplemented()

    print request.json_body
    movie = Movies.by_id(request.json_body.get('id'))

    if not movie:
        return HTTPBadRequest()

    command = streamer.format(movie.path)

    subprocess.Popen(shlex.split(command))

    return HTTPAccepted()
