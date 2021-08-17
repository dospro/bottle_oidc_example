import bottle
from bottle import Bottle, run, template, request, response, redirect

from views.oidc import OIDCPlugin

bottle.TEMPLATE_PATH = ["./templates/"]
PUBLIC_ROUTES = ["/login", "/callback"]

app = Bottle()

app.install(OIDCPlugin())


@app.route('/', method='get')
def home():
    user = request.user
    return template("index", name=user)


run(app, host='localhost', port=8000, debug=True, reloader=True)
