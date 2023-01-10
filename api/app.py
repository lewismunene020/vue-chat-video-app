from flask import Flask, jsonify, request
from database import Database
from story_fetcher import StoryFetcher
from interest_predictor import InterestPredictor
from call import VideoCall

app = Flask(__name__)

# Initialize the Database, StoryFetcher, and InterestPredictor classes
db = Database()
sf = StoryFetcher()
ip = InterestPredictor()
vc = VideoCall()

@app.route("/send_message", methods=["POST"])
def send_message():
    # Get the message and user ID from the request
    message = request.json["message"]
    user_id = request.json["user_id"]

    # Predict the user's interests
    ip.predict_interests(message, user_id)

    # Store the message in the database
    db.store_message(message, user_id)

    # Return a success message
    return jsonify({"status": "success"})

@app.route("/fetch_stories", methods=["GET"])
def fetch_stories():
    # Get the user ID from the request
    user_id = request.args.get("user_id")

    # Get the user's interests
    interests = ip.get_user_interests(user_id)

    # Fetch the stories that match the user's interests
    stories = sf.get_interesting_stories(interests)

    # Return the stories to the client
    return jsonify({"stories": stories})

@app.route("/call", methods=["POST"])
def call():
    call_type = request.json["type"]
    caller_id = request.json["caller_id"]
    receiver_id = request.json["receiver_id"]
    if call_type == 'video':
        vc.make_video_call(caller_id, receiver_id)
        return jsonify({"status": "Video call initiated"})
    else:
        return jsonify({"status": "Invalid call type"})

if __name__ == '__main__':
    app.run(debug=True)
