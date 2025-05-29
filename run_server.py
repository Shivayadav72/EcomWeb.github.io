from waitress import serve
from ecom.wsgi import application
serve(application, host='0.0.0.0',port=8080)