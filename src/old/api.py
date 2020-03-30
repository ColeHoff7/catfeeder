from flask import Flask
from flask_restful import reqparse, Resource, Api
from feed import Feed

app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('morning')
parser.add_argument('night')

class Feeder(Resource):
    morning = None
    m_schedule = None
    night = None
    n_schedule = None

    def get(self):
        return {'hello': 'porko'}
    
    def post(self):
        args = parser.parse_args()
        morning = Feed(args.morning)
        night = Feed(args.night)
        m_schedule = morning.start_schedule()
        n_schedule = night.start_schedule()

api.add_resource(Feeder, '/porko')

if __name__ == '__main__':
    app.run(debug=True)