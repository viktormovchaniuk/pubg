# from pyramid.request import Response
# from pyramid.request import Request
from pyramid.config import Configurator


from pyramid.events import NewRequest


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.routes')
        config.include('.models')
        config.include('.security')
        config.include('pyramid_jinja2')
        config.include('pyramid_mailer')
        config.include('pyramid_layout')
        config.add_layout('pubg_project.layout.Layout',
                          'pubg_project.layout:templates/layout.jinja2')
        config.scan()
    return config.make_wsgi_app()
