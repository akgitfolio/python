from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)
from confluent_kafka import Producer
from confluent_kafka.admin import AdminClient, NewTopic
import json
import time

app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "your_secret_key"
app.config["JWT_SECRET_KEY"] = "your_jwt_secret_key"


db = SQLAlchemy(app)
jwt = JWTManager(app)


TOPIC_NAME = "auth_logs"


def create_kafka_topic(topic_name, num_partitions=1, replication_factor=1):
    admin_client = AdminClient({"bootstrap.servers": "localhost:9092"})
    topic_metadata = admin_client.list_topics(timeout=5)

    if topic_name in topic_metadata.topics:
        print(f"Topic {topic_name} already exists")
    else:
        print(f"Creating topic {topic_name}")
        new_topic = NewTopic(
            topic_name,
            num_partitions=num_partitions,
            replication_factor=replication_factor,
        )
        admin_client.create_topics([new_topic])
        print(f"Topic {topic_name} created successfully")


producer = Producer({"bootstrap.servers": "localhost:9092"})


def delivery_report(err, msg):
    """Callback called once message is delivered to Kafka"""
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def log_auth_event(success, username, response_time, status_code, request_info):
    """Log authentication event to Kafka"""
    event = {
        "event": "authentication",
        "username": username,
        "success": success,
        "response_time": response_time,
        "status_code": status_code,
        "request_info": request_info,
    }
    producer.produce(
        TOPIC_NAME, key=username, value=json.dumps(event), callback=delivery_report
    )
    producer.poll(1)


@app.before_request
def auth_middleware():
    if request.endpoint == "login" and request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user_agent = request.headers.get("User-Agent")
        origin_ip = request.remote_addr
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        start_time = time.time()
        user = User.query.filter_by(username=username).first()
        response_time = time.time() - start_time

        if user and check_password_hash(user.password, password):
            success = True
            status_code = 200
        else:
            success = False
            status_code = 401

        request_info = {
            "method": request.method,
            "path": request.path,
            "query_params": request.args.to_dict(),
            "headers": dict(request.headers),
            "cookies": request.cookies,
            "timestamp": timestamp,
            "http_version": request.environ.get("SERVER_PROTOCOL"),
            "content_type": request.content_type,
            "accept": request.headers.get("Accept"),
            "user_agent": user_agent,
            "origin_ip": origin_ip,
        }

        log_auth_event(success, username, response_time, status_code, request_info)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


with app.app_context():
    db.create_all()
    create_kafka_topic(TOPIC_NAME)


@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Username and password required"}), 400

    username = data["username"]
    password = data["password"]

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "User already exists"}), 409

    hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
    new_user = User(username=username, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"msg": "Username and password required"}), 400

    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Invalid credentials"}), 401

    access_token = create_access_token(identity={"username": user.username})
    return jsonify(access_token=access_token), 200


@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


if __name__ == "__main__":
    app.run(debug=True)
