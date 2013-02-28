from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPNotFound

from mako.exceptions import TopLevelLookupException

from .models import (
    DBSession,
    Movies,
)

@view_config(route_name='home', renderer='index.mako')
def home(request):
    return {
        'api_key': request.registry.settings['movie.api_key']
    }

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
