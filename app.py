from flask import Flask
from flask import request
from image_classifier.classification_model import scene_detection
from itinerary_generator.main import generateItineries
from urllib.parse import unquote

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
    generateItineries()
    return "hello"


if __name__ == "__main__":
    app.run()
