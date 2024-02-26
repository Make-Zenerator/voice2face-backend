from flask import Flask, request
from flask_cors import CORS
from flask_restx import Api
from db.db_connection import db_connection, db
# from prometheus_flask_exporter import PrometheusMetrics
from apis_v1 import User, MzRequest

app = Flask(__name__)
# app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 용량제한
app.config.update(DEBUG=True)

CORS(app, resources={r'*': {'origins': '*'}})

db_connection(app)
with app.app_context():
    db.create_all()
# metrics = PrometheusMetrics.for_app_factory()
# metrics.init_app(app)

api = Api(
    app,
    version='v1',
    title="Make Generator",
    description="NAVER boostcamp",
    terms_url="/",
    contact="vivian0304@naver.com",
    license="MIT",
    prefix='/api/v1'
)

api.add_namespace(User.Users, '/users')
api.add_namespace(User.Auth, '/auth')
api.add_namespace(MzRequest.MzRequest, '/mz-request')

if __name__ == "__main__":
    app.run(port=5050, debug=True)
