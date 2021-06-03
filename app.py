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

    if int(request.args.get("personalised")) == 0:

        is_personalised = False

        x = generateItineries(moderation, days, is_personalised)

    else:

        is_personalised = True

        beach = int(request.args.get("beach"))
        clubbing = int(request.args.get("clubbing"))
        nature = int(request.args.get("nature"))
        shopping = int(request.args.get("shopping"))
        museums = int(request.args.get("museums"))
        bars = int(request.args.get("bars"))

        x = generateItineries(
            moderation,
            days,
            is_personalised,
            beach,
            clubbing,
            bars,
            nature,
            shopping,
            museums,
        )

    response = jsonify(x.to_dict())
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response


if __name__ == "__main__":
    app.run()
