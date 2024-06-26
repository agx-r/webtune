from flask import request, Flask, render_template, send_from_directory, abort, Blueprint, redirect, url_for
from flask_restx import Api
from media_routes import ns as media_namespace
from media_routes import player
from logger import setup_logger
from dbcontroller import DatabaseConnector
from config_updater import load_config
import threading
import requests
import time

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Load config once during startup
config = load_config()

# Setup logger
logger = setup_logger()

# Create a Blueprint for the main routes
main_blueprint = Blueprint('main_blueprint', __name__, template_folder='templates', static_folder='static')

# Initialize Flask-Restx API
api = Api(app, version='1.0', title='Media Player API', description='A simple Media Player API', doc='/api/docs')

# Add media namespace to the API
api.add_namespace(media_namespace)

# Dictionary to map routes to templates
page_templates = {
    'credentials': 'credentials.html',
    'index': 'index.html',
    'main': 'index.html',
    'local-media': 'local-media.html',
    'public-announcement': 'public-announcement.html',
    'info': 'info.html',
    'stream-collections': 'stream-collections.html',
}

# Route for serving static files
@main_blueprint.route('/static/<path:folder>/<path:filename>')
def serve_static(folder, filename):
    return send_from_directory('static', f'{folder}/{filename}')

# Route for rendering other pages
@main_blueprint.route('/<page>')
def render_page(page):
    logger.info(f'Route /{page}')
    config = load_config()
    template = page_templates.get(page)
    if not template:
        abort(404)
    return render_template(template,
        current_player_link=f"{config.get('preview_url', '')}/embed?theme=dark",
        client_id=config.get('client_id', ''),
        device_id=config.get('device_id', ''),
        password=config.get('password', ''),
        request=request
    )

# Redirect from / to /main
@app.before_request
def redirect_main():
    if request.path == '/':
        return redirect(url_for('main_blueprint.render_page', page='main'), code=302)

def is_server_available(url):
    try:
        response = requests.head(url, timeout=10)
        if response.status_code < 400:
            return True
        else:
            return False
    except requests.RequestException:
        return False

def start_periodic_check():
    check_thread = threading.Thread(target=check_server_periodically)
    check_thread.daemon = True
    check_thread.start()

def check_server_periodically():
    restart_next_time = False
    while True:
        url = load_config()['stream_url']

        is_playing = not player.core_idle
        logger.debug(f"Playing status: {is_playing}")

        if is_playing:
            available = is_server_available(url)
            if available:
                logger.debug(f"The stream is available")
                if restart_next_time:
                    restart_next_time = False
                    player.play(url)
            else:
                logger.debug(f"The stream is unavailable")
                restart_next_time = True
                player.play(url)
        
        time.sleep(10)

# Register blueprint
app.register_blueprint(main_blueprint)

if __name__ == '__main__':
    config = load_config()
    start_periodic_check()
    app.run(host='0.0.0.0', port=80, debug=False)
