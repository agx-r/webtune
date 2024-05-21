import mpv
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from logger import setup_logger
from dbcontroller import DatabaseConnector

app = Flask(__name__)
api = Api(app, version='1.0', title='Media Player API', description='A simple Media Player API')
ns = api.namespace('media', description='Media operations')

player = mpv.MPV()
logger = setup_logger()

db_connector = DatabaseConnector(host='your_host', user='your_user', password='your_password', database='your_database')

# Define the expected input for the play endpoint
play_model = api.model('Play', {
    'url': fields.String(required=True, description='The URL of the media to play')
})

# Define the expected input for the volume endpoint
volume_model = api.model('Volume', {
    'volume': fields.Integer(required=True, description='The volume level to set', min=0, max=100)
})

# Define the expected input for retrieving data by client and device IDs
data_model = api.model('Data', {
    'client_id': fields.String(required=True, description='The client ID'),
    'device_id': fields.String(required=True, description='The device ID')
})

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

if __name__ == '__main__':
    app.run(debug=True)
