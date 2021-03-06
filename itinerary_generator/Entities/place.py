import json
import requests
import requests_cache

from itinerary_generator.Entities.hours import Hours
from itinerary_generator.Entities.characteristics import Characteristic
from itinerary_generator.Entities.location import Location
from itinerary_generator.Entities.Enums.transport import Transport
from itinerary_generator.Entities.rating import Rating
from itinerary_generator.Entities.Enums.category import Category
from itinerary_generator.Entities.category_constant import Category_Constant
from itinerary_generator.Entities.Enums.price import Price
from os import listdir
from os.path import isfile, join

day_id = 0
night_id = 0
cafe_id = 0
restaurant_id = 0


requests_cache.install_cache("demo_cache")


class Place:

    cafe_places_by_id = {}
    restaurant_places_by_id = {}
    day_places_by_id = {}
    night_places_by_id = {}
    places_of_category = {}

    def __init__(
        self,
        name: str = None,
        hours: Hours = None,
        price: Price = None,
        rating: Rating = None,
        no_of_ratings: int = None,
        location: Location = None,
        category: Category = None,
        place_name=None,
        time=None,
        type=None,
    ):

        super().__init__()
        global day_id
        global night_id
        global cafe_id
        global restaurant_id

        self.name = name
        self.hours = hours
        self.price = price
        self.rating = rating
        self.no_of_ratings = no_of_ratings
        self.location = location
        self.category = category
        self.place_name = place_name

        if type != 0:
            if type == 1:
                self.id = day_id
                Place.day_places_by_id[self.id] = self
                day_id += 1
            elif type == 2:
                self.id = night_id
                Place.night_places_by_id[self.id] = self
                night_id += 1
            elif type == 3:
                self.id = cafe_id
                Place.cafe_places_by_id[self.id] = self
                cafe_id += 1
            elif type == 4:
                self.id = restaurant_id
                Place.restaurant_places_by_id[self.id] = self
                restaurant_id += 1

        Place.places_of_category[category].append(self)

        if time is not None:
            self.time = time

    def time_to(self, place_two):

        url = "http://127.0.0.1:5000/table/v1/driving/"
        url = url + str(self.location.y) + "," + str(self.location.x) + ";"
        url = url + str(place_two.location.y) + "," + str(place_two.location.x)
        duration = requests.get(url).json()
        if duration["durations"][0][1] is None:
            duration_time = 0
        else:
            duration_time = (duration["durations"][0][1]) / 60

        # distance = geopy.distance.geodesic(
        #     place_one_location, place_two_location).m
        # avg_speed = 13.8889

        # time = distance / avg_speed
        # if time != 0:
        #     time = time + 1000

        # time = datetime.timedelta(seconds=time)

        return duration_time, Transport.car

    @staticmethod
    def set_places(characteristics):

        Place.cafe_places_by_id = {}
        Place.restaurant_places_by_id = {}
        Place.day_places_by_id = {}
        Place.night_places_by_id = {}
        Place.places_of_category = {}

        global day_id
        global night_id
        global cafe_id
        global restaurant_id

        day_id = 0
        night_id = 0
        cafe_id = 0
        restaurant_id = 0

        for i in Category:
            Place.places_of_category[i] = []

        path = "itinerary_generator/NearbySearch/beach/"
        create_place(path, Category.beach, characteristics, type=1)

        path = "itinerary_generator/NearbySearch/museums/"
        create_place(path, Category.museums, characteristics, type=1)

        path = "itinerary_generator/NearbySearch/nature/"
        create_place(path, Category.nature, characteristics, type=1)

        path = "itinerary_generator/NearbySearch/shopping/"
        create_place(path, Category.shopping, characteristics, type=1)

        path = "itinerary_generator/NearbySearch/night_clubs/"
        create_place(path, Category.club, characteristics, type=2)

        path = "itinerary_generator/NearbySearch/bars/"
        create_place(path, Category.bar, characteristics, type=2)

        path = "itinerary_generator/NearbySearch/cafeterias/"
        create_place(path, Category.cafe, characteristics, type=3)

        path = "itinerary_generator/NearbySearch/restaurants/"
        create_place(path, Category.restaurant, characteristics, type=4)

    @staticmethod
    def of_category(category):
        return Place.places_of_category[category]

    @staticmethod
    def remove_place(category, place):
        Place.places_of_category[category].remove(place)

    @staticmethod
    def delete_place(category, place, days):
        place_id = place.id
        Place.places_of_category[category].remove(place)

        morning = [Category.nature, Category.shopping, Category.museums, Category.beach]
        evening = [Category.club, Category.bar]

        if category == Category.cafe:
            Place.cafe_places_by_id = tool_for_delete(
                place_id, Place.cafe_places_by_id, days
            )

        if category == Category.restaurant:
            Place.restaurant_places_by_id = tool_for_delete(
                place_id, Place.restaurant_places_by_id, days
            )

        if category in morning:
            Place.day_places_by_id = tool_for_delete(
                place_id, Place.day_places_by_id, days
            )

        if category in evening:
            Place.night_places_by_id = tool_for_delete(
                place_id, Place.night_places_by_id, days
            )

    @staticmethod
    def readd_place(place):
        Place.places_of_category[place.category].append(place)


def tool_for_delete(place_id, dictionary, days):

    for i in range((place_id + 1), len(dictionary)):
        # breakpoint()
        place = dictionary[i]

        for index, temp_place_id in enumerate(days):
            if temp_place_id == i:
                days[index] = i - 1
        dictionary[i].id = i - 1
        dictionary[i - 1] = place

    dictionary.pop((len(dictionary) - 1), None)
    return dictionary


def create_place(path, category, characteristics: Characteristic, type):

    results = [f for f in listdir(path) if isfile(join(path, f))]

    for i in results:

        f = open(path + i,)
        x = json.load(f)

        for i in x["results"]:

            if "rating" in i:

                name = i["name"]
                rating = i["rating"]
                no_of_ratings = i["user_ratings_total"]
                longitude = i["geometry"]["location"]["lng"]
                latitude = i["geometry"]["location"]["lat"]
                location = Location(latitude, longitude)
                price_level = None

                if "price_level" in i:
                    price_level = i["price_level"]

                if "vicinity" in i:
                    vicinity = i["vicinity"].split(",")[-1]
                else:
                    vicinity = ""

                time = calculate_time(characteristics, rating, category)

                Place(
                    name=name,
                    price=price_level,
                    rating=rating,
                    no_of_ratings=no_of_ratings,
                    category=category,
                    location=location,
                    time=time,
                    place_name=vicinity,
                    type=type,
                )


def calculate_time(characteristics, rating, category):
    userPref = characteristics.get_value_by_category(category)
    if userPref == None:
        userPref = 1
    else:
        userPref = userPref / 100

    rating = (rating * 20) / 100

    time = (userPref + rating) * Category_Constant[category]
    time = 0.5 * round(float(time) / 0.5)
    return time


for i in Category:
    Place.places_of_category[i] = []
