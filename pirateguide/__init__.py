from pyramid.config import Configurator

from sqlalchemy import engine_from_config

from webassets import Bundle

from .models import (
    DBSession,
    Base,
)

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """

    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    config = Configurator(settings=settings)

    config.add_static_view('static', 'static', cache_max_age=3600)

    config.add_route('home', '/')
    config.add_route('partials', '/partials/{partial}.html')

    config.add_route('movie.list', '/movies')
    config.add_route('movie.play', '/movies/play')

    js_bundle = Bundle('js/*.js',
                       filters='rjsmin', output='js/app.min.js', debug=False)
    less_bundle = Bundle('css/app.less',
                         filters='less', output='css/app.min.css', debug=False)

    config.add_webasset('js', js_bundle)
    config.add_webasset('less', less_bundle)

    config.scan()

    return config.make_wsgi_app()
