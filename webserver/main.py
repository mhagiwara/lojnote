import os

import pystache
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.asset import resolve_asset_spec
from pyramid.view import view_config
from pyramid.path import package_path


class MustacheRendererFactory(object):
    def __init__(self, info):
        self.info = info

    def __call__(self, value, system):
        package, filename = resolve_asset_spec(self.info.name)
        template = os.path.join(package_path(self.info.package), filename)
        template_fh = open(template)
        template_stream = template_fh.read()
        template_fh.close()
        return pystache.render(template_stream, value)


@view_config(route_name='hello')
def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)


@view_config(route_name='hello2', renderer='hello_world.tmpl')
def hello_world2(request):
    return dict(name=request.matchdict['name'])


if __name__ == '__main__':
    config = Configurator()
    config.add_renderer(name='.tmpl', factory='webserver.main.MustacheRendererFactory')
    config.add_route('hello', '/hello/{name}')
    config.add_route('hello2', '/hello2/{name}')
    config.scan()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8180, app)
    server.serve_forever()
