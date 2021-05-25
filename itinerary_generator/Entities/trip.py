import itinerary_generator.Optimiser.pso as pso

from itinerary_generator.Entities.Enums.budget import Budget
from itinerary_generator.Entities.place import Place


class Trip:
    """
    From this trip object a user will be able to generate itineraries
    that are applicable to his constraints. Constraints include:
    budget, moderation, characteristics, travel date and accomodation.
    """

    def __init__(
        self,
        budget: Budget,
        moderation,
        characteristics,
        number_of_days,
        accomodation: Place,
    ):
        super().__init__()

        self.budget = budget
        self.moderation = moderation
        self.characteristics = characteristics
        self.number_of_days = number_of_days
        self.accomodation = accomodation

    def generate_itineraries(self):

        return pso.Optimse(self)

