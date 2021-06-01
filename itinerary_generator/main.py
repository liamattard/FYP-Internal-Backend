import datetime

from itinerary_generator.Entities.location import Location
from itinerary_generator.Entities.Enums.category import Category
from itinerary_generator.Entities.place import Place
from itinerary_generator.Entities.trip import Trip
from itinerary_generator.Entities.characteristics import Characteristic
from itinerary_generator.Entities.timetable import Timetable


def generateItineries(
    moderation, number_of_days, beach, clubbing, bars, nature, shopping, museums
):

    accomodation = Place(
        name="Hotel",
        category=Category.accomodation,
        location=Location(35.8988, 14.5124),
        type=0,
    )

    characteristics = Characteristic(
        beach=beach,
        museums=museums,
        nature=nature,
        clubbing=clubbing,
        bar=bars,
        shopping=shopping,
    )

    trip = Trip(
        budget=3,
        moderation=moderation,
        characteristics=[characteristics],
        number_of_days=number_of_days,
        accomodation=accomodation,
    )

    Place.set_places(trip.characteristics[0])
    return trip.generate_itineraries()

