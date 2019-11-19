from flask import Flask, Response

from config import get_config
from db import db

app = Flask(__name__)
app.config.from_object(get_config())
db.init_app(app)

@app.route('/health')
def health_check():
    return Response(status=200)

if __name__ == '__main__':
    app.run(debug=True)