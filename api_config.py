from flask_restx import fields, Namespace

# Create namespace
ns = Namespace('media', description='Media operations')

# Define the expected input for the play endpoint
play_model = ns.model('Play', {
    'url': fields.String(required=True, description='The URL of the media to play')
})

# Define the expected input for the volume endpoint
volume_model = ns.model('Volume', {
    'volume': fields.Integer(required=True, description='The volume level to set', min=0, max=100)
})

# Define the expected input for retrieving data by client and device IDs
data_model = ns.model('Data', {
    'client_id': fields.String(required=True, description='The client ID'),
    'device_id': fields.String(required=True, description='The device ID')
})
