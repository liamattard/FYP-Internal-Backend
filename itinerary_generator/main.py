import datetime

from itinerary_generator.Entities.location import Location
from itinerary_generator.Entities.Enums.category import Category
from itinerary_generator.Entities.place import Place
from itinerary_generator.Entities.trip import Trip
from itinerary_generator.Entities.characteristics import Characteristic
from itinerary_generator.Entities.timetable import Timetable


def generateItineries():

    accomodation = Place(
        name="Hotel",
        category=Category.accomodation,
        location=Location(35.8988, 14.5124),
        type=0,
    )

    characteristics = Characteristic(
        beach=1, museums=4, nature=1, clubbing=7, bar=2, shopping=8,
    )

    dateStart = datetime.datetime(2021, 5, 17)
    dateFinal = datetime.datetime(2021, 5, 18)

    trip = Trip(
        budget=3,
        moderation=3,
        characteristics=[characteristics],
        date=[dateStart, dateFinal],
        accomodation=accomodation,
    )

    Place.set_places(trip.characteristics[0])
    trip.generate_itineraries()
    trip.generate_itineraries()
    trip.generate_itineraries()
    trip.generate_itineraries()
    trip.generate_itineraries()
    trip.generate_itineraries()
    trip.generate_itineraries()
