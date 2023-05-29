from flask import Flask, render_template, redirect, url_for, flash, request, abort
import flask.cli
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import argparse
from os import urandom
from urllib.parse import urlparse, urljoin

from prgrmUtils.Logger import LoggerService

# ======================================================================================================
app = Flask(__name__)
secretKey = urandom(32).hex()
logger = LoggerService("logs.db", False).info("Server", "Server started with secret key: " + secretKey)
app.config['SECRET_KEY'] = secretKey
login_manager = LoginManager()
login_manager.init_app(app)
# ======================================================================================================

class User(UserMixin):
    def __init__(self, id=None):
        self.id = id
    
    def get_id(self):
        return self.id

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@login_manager.unauthorized_handler
def unauthorized():
    logger.insertWebLog("Unregistered",f"Unauthorized access to {request.path} from {request.remote_addr}")
    flash('Vous devez être connecté pour accèder à cette page !', 'warning')
    return redirect('/login?next=' + request.path)

@app.errorhandler(400)
def bad_request(e):
    logger.insertErrorLog(current_user.id,f"Bad request from {request.remote_addr} on {request.path} : {e}")
    flash("Requête invalide, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="400", ErrorMsg="Requête invalide"), 400

@app.errorhandler(404)
def page_not_found(e):
    logger.insertErrorLog(current_user.id,f"Page not found from {request.remote_addr} on {request.path} : {e}")
    flash("Page introuvable, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="404", ErrorMsg="Page introuvable"), 404

@app.errorhandler(500)
def internal_server_error(e):
    logger.insertErrorLog(current_user.id,f"Internal server error from {request.remote_addr} on {request.path} : {e}")
    flash("Erreur interne, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="500", ErrorMsg="Erreur interne, l'accès a cette page a fini sur une erreur."), 500

@app.errorhandler(502)
def bad_gateway(e):
    logger.insertErrorLog(current_user.id,f"Bad gateway from {request.remote_addr} on {request.path} : {e}")
    flash("Erreur interne, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="502", ErrorMsg="Erreur interne, l'accès a cette page a fini sur une erreur."), 502

@app.errorhandler(503)
def service_unavailable(e):
    logger.insertErrorLog(current_user.id,f"Service unavailable from {request.remote_addr} on {request.path} : {e}")
    flash("Erreur interne, si vous estimez que cela n'est pas normal, contactez l'administrateur.", 'danger')
    return render_template('error.html', ErrorCode="503", ErrorMsg="Erreur interne, l'accès a cette page a fini sur une erreur."), 503

@app.route("/")
def index():
    return render_template('index.html')