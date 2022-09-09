import os

from app import create_app, register_blueprints, attach_middleware
from flask_cors import CORS
# from authlib.integrations.flask_client import OAuth


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
register_blueprints(app)
attach_middleware(app)
# oauth = OAuth(app)

api_v1_cors_config = {
  "methods": ["OPTIONS", "GET", "POST", "PUT", "DELETE"],
}
CORS(app, resources={"*": api_v1_cors_config})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', os.getenv('PORT')))

