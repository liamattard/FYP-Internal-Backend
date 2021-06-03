import datetime

from itinerary_generator.Entities.location import Location
from itinerary_generator.Entities.Enums.category import Category
from itinerary_generator.Entities.place import Place
from itinerary_generator.Entities.trip import Trip
from itinerary_generator.Entities.characteristics import Characteristic
from itinerary_generator.Entities.timetable import Timetable


def generateItineries(
    moderation,
    number_of_days,
    is_personalised,
    beach=None,
    clubbing=None,
    bars=None,
    nature=None,
    shopping=None,
    museums=None,
):

    accomodation = Place(
        name="Hotel",
        category=Category.accomodation,
        location=Location(35.8988, 14.5124),
        type=0,
    )

    characteristics = None

    if is_personalised:

        characteristics = Characteristic(
            beach=beach,
            museums=museums,
            nature=nature,
            clubbing=clubbing,
            bar=bars,
            shopping=shopping,
        )

    else:

        characteristics = Characteristic(
            beach=1, museums=1, nature=1, clubbing=1, bar=1, shopping=1,
        )

    trip = Trip(
        budget=3,
        moderation=moderation,
        characteristics=[characteristics],
        number_of_days=number_of_days,
        accomodation=accomodation,
        is_personalised=is_personalised,
    )

    Place.set_places(trip.characteristics[0])
    return trip.generate_itineraries()

