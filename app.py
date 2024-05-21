import mpv
from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from logger import setup_logger

app = Flask(__name__)
api = Api(app, version='1.0', title='Media Player API', description='A simple Media Player API')
ns = api.namespace('media', description='Media operations')

player = mpv.MPV()
logger = setup_logger()

# Define the expected input for the play endpoint
play_model = api.model('Play', {
    'url': fields.String(required=True, description='The URL of the media to play')
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

if __name__ == '__main__':
    app.run(debug=True)
