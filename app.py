from flask import Flask
from flask import request
from flask import jsonify
from image_classifier.classification_model import scene_detection
from itinerary_generator.main import generateItineries
from urllib.parse import unquote
from itinerary_generator.Entities.timetable import Timetable

app = Flask(__name__)


@app.route("/classify_image")
def main():
    url = request.args.get("url")
    decoded_url = unquote(url)
    print("Recieved URL: ", decoded_url)
    print("\n...")
    scene = scene_detection(decoded_url)
    return scene


@app.route("/generate_itineraries")
def timetable():
    moderation = int(request.args.get("moderation"))
    days = int(request.args.get("days"))
    x = generateItineries(moderation, days)
    response = jsonify(x.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run()
