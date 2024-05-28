import mpv
from flask import request, jsonify
from flask_restx import Resource
from api_config import ns, play_model, volume_model, data_model
from logger import setup_logger
from dbcontroller import DatabaseConnector
from config_updater import load_config

# Initialize MPV player
player = mpv.MPV()
logger = setup_logger()

# Initialize database connector
db_connector = DatabaseConnector(host='your_host', user='your_user', password='your_password', database='your_database')

@ns.route('/play')
class Play(Resource):
    @ns.expect(play_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error')
    def post(self):
        """Play media from a given URL"""
        data = request.json
        url = data.get('url')
        if not url:
            ns.abort(400, 'URL is required')
        player.play(url)
        logger.info(f"Playing: {url}")
        return jsonify({'message': 'Playing'})

@ns.route('/stop')
class Stop(Resource):
    @ns.response(200, 'Success')
    def post(self):
        """Stop playing media"""
        player.stop()
        logger.info("Stopped")
        return jsonify({'message': 'Stopped'})

@ns.route('/play_current')
class PlayCurrent(Resource):
    @ns.response(200, 'Success')
    def post(self):
        """Use URL from config"""
        config = load_config()
        url_to_play = config["stream_url"]
        player.stop()
        player.play(url_to_play)
        logger.info(f"Playing {url_to_play}")
        return jsonify({'message': f'Playing {url_to_play}'})

@ns.route('/volume')
class Volume(Resource):
    @ns.expect(volume_model)
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error')
    def post(self):
        """Change the volume level"""
        data = request.json
        volume = data.get('volume')
        if volume is None or not (0 <= volume <= 100):
            ns.abort(400, 'Volume must be an integer between 0 and 100')
        player.volume = volume
        logger.info(f"Volume set to: {volume}")
        return jsonify({'message': 'Volume set', 'volume': volume})

@ns.route('/retrieve_data/<string:client_id>/<string:device_id>')
class RetrieveData(Resource):
    @ns.response(200, 'Success')
    @ns.response(400, 'Validation Error')
    def get(self, client_id, device_id):
        """Retrieve data from the database"""
        result = db_connector.retrieve_data(client_id, device_id)
        if result is None:
            ns.abort(400, 'Data not found or an error occurred')
        return jsonify({'data': result})
