# -*- coding: utf-8 -*-

from flask import Flask, Blueprint
from flask_httpauth import HTTPBasicAuth
from flask_restplus import abort, Api, Resource, apidoc
from dateutil.parser import parse as dtparse
from datetime import datetime, timedelta

import numpy as np
import cv2
import flask
import StringIO
import os
import json


# Nome do servico da API
_SNAME = 'teste'

# Criando a aplicação web
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/'+_SNAME)
api = Api(blueprint, ui=False, version='1.0', title='Teste', default=_SNAME, default_label=u'',
          description=u'Isto é uma descrição.')
auth = HTTPBasicAuth()

# Configurando autenticação
@auth.get_password
def get_password(username):
    if username == 'admin':
        return '123456'
    return None
    

class Root(Resource):
    def get(self):
        start_response('200 OK', [('Content-Type','text/html')])
        return "Olá."


class Hello(Resource):
    """ Apenas indica que conexão está ok. """
    decorators = [auth.login_required]

    def get(self):
        u"""Teste de conexão e autenticação"""
        return {'service_status': 'ok'}


class Echo(Resource):
    def get(self, msg):
	    return 'A mensagem é: {}'.format(msg)


# Mapeando os recursos da API
api.add_resource(Hello, '/hello')
api.add_resource(Echo, '/echo/<msg>')
#api.add_resource(Root, '/')

# Documentação swagger
@blueprint.route('/doc')
def swagger_ui():
    return apidoc.ui_for(api)
app.register_blueprint(blueprint)

    
if __name__ == '__main__':
    app.run(debug=True)
