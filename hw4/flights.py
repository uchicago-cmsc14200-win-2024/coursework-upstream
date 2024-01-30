"""
Module providing an Airport and Flight classes, as well as some
supporting data types. This module also includes functions to
create sample schedules described in the homework writeup.
"""
from enum import IntEnum


class TimeOfDay(IntEnum):
    """
    Enumerated type for the four time periods we will
    work with in our flight schedules
    """
    MORNING = 0
    AFTERNOON = 1
    EVENING = 2
    NIGHT = 3


class Airport:
    """
    Class representing an individual airport
    """

    __name: str
    __code: str
    __flights: dict[str, "Flight"]

    def __init__(self, name: str, code: str):
        """
        Constructor

        Args:
            name: Airport's name
            code: Airport's 3-letter code
        """
        assert len(code) == 3 and all(c.isupper() for c in code), \
            "Airport codes must be three uppercase letters"

        self.__name = name
        self.__code = code

        self.__flights = {}

    def __str__(self) -> str:
        """
        Returns: String representation of airport
        """
        return f"{self.__name} ({self.__code})"

    def __repr__(self) -> str:
        """
        Returns: String representation of airport
        """
        return str(self)

    def __lt__(self, other: "Airport") -> bool:
        """
        If we need to sort airports at any point, we will
        do so by the airport code. This means that, in algorithms
        like Dijkstra's, the tie-breaker in a priority queue
        (for entries with the same cost) will be the airport's code.
        """
        return self.code < other.code

    @property
    def name(self) -> str:
        """
        Returns: Airport's name
        """
        return self.__name

    @property
    def code(self) -> str:
        """
        Returns: Airport's 3-letter code
        """
        return self.__code

    @property
    def flights(self) -> set["Flight"]:
        """
        Returns: Flights departing from this airport
        """
        return set(self.__flights.values())

    def add_flight(self, flight: "Flight") -> None:
        """
        Adds a flight to the set of flights departing
        from this airport.

        Args:
            flight:

        Returns:

        """
        error_msg = f"Can't add flight {flight} to airport {self.__code}. " \
                    f"Origin airport ({flight.origin.code}) does not match."
        assert flight.origin == self, error_msg

        self.__flights[flight.code] = flight

    def get_flight_by_code(self, code: str) -> "Flight":
        """
        Given a flight code, returns the Flight object if
        such a flight departs from this airport; raises
        a ValueError exception otherwise.

        Args:
            code: Flight code (two letters followed by four digits,
            e.g., UC0001)

        Raises:
            ValueError: If no flight with that code departs from
            the airport

        Returns: Flight object for the provided code (if one exists,
        and it departs from this airport)

        """
        if code not in self.__flights:
            raise ValueError(f"{self.__code} has no such flight: {code}")

        return self.__flights[code]


class Flight:
    """
    Class representing an individual flight.
    """

    __origin: Airport
    __destination: Airport
    __airline: str
    __flight_num: int
    __departure_time: TimeOfDay
    __cost: int

    def __init__(self, origin: Airport, destination: Airport, airline: str,
                 flight_num: int, departure_time: TimeOfDay, cost: int):
        """
        Constructor

        Args:
            origin: Airport the flight departs from
            destination: Airport the flight arrives at
            airline: Airline code (2-letter string)
            flight_num: Flight number (between 1 and 9999)
            departure_time: Time the flight departs
            cost: Cost in dollars of the flight
        """
        assert origin != destination
        assert len(airline) == 2, "Airline codes have two characters"
        assert flight_num < 10000, "Flight numbers have at most 4 digits"
        assert cost > 0, "The cost of a flight must be greater than zero"

        self.__origin = origin
        self.__destination = destination
        self.__airline = airline
        self.__flight_num = flight_num
        self.__departure_time = departure_time
        self.__cost = cost

    def __str__(self) -> str:
        """
        Returns: String representation of flight
        """
        return f"{self.code}: {self.__origin.code} -> " \
               f"{self.__destination.code} @ {self.__departure_time.name}"

    def __repr__(self) -> str:
        """
        Returns: String representation of flight
        """
        return str(self)

    def __lt__(self, other: "Flight") -> bool:
        """
        If we need to sort flights at any point, we will
        do so by the flight code.
        """
        return self.code < other.code

    @property
    def origin(self) -> Airport:
        """
        Returns: The airport the flight departs from
        """
        return self.__origin

    @property
    def destination(self) -> Airport:
        """
        Returns: The airport the flight arrives at
        """
        return self.__destination

    @property
    def airline(self) -> str:
        """
        Returns: The airline code of the flight
        """
        return self.__airline

    @property
    def flight_num(self) -> int:
        """
        Returns: The flight number of the flight
        """
        return self.__flight_num

    @property
    def code(self) -> str:
        """
        Returns: The flight code. This is the airline code followed
        by the flight number (if the flight number has less than 4 digits,
        it is padded with zeros on the left)
        """
        return f"{self.__airline}{self.__flight_num:04}"

    @property
    def departure_time(self) -> TimeOfDay:
        """
        Returns: The departure time of the flight
        """
        return self.__departure_time

    @property
    def cost(self) -> int:
        """
        Returns: The cost of the flight
        """
        return self.__cost


def sample_schedule_1() -> dict[str, Airport]:
    """
    Returns: Sample schedule described in the "Flight Schedules" section
    of the homework writeup.
    """

    ord = Airport("Chicago O'Hare", "ORD")  # pylint: disable=redefined-builtin
    lga = Airport("New York LaGuardia", "LGA")
    lax = Airport("Los Angeles International", "LAX")
    sfo = Airport("San Francisco International", "SFO")

    ord.add_flight(Flight(ord, lga, "UC", 1, TimeOfDay.MORNING, 200))
    ord.add_flight(Flight(ord, lga, "UC", 2, TimeOfDay.AFTERNOON, 100))

    lga.add_flight(Flight(lga, lax, "UC", 3, TimeOfDay.MORNING, 200))
    lga.add_flight(Flight(lga, lax, "UC", 4, TimeOfDay.AFTERNOON, 300))

    lax.add_flight(Flight(lax, lga, "UC", 5, TimeOfDay.NIGHT, 5000))
    lax.add_flight(Flight(lax, sfo, "UC", 6, TimeOfDay.EVENING, 100))

    sfo.add_flight(Flight(sfo, ord, "UC", 7, TimeOfDay.NIGHT, 350))

    return {"ORD": ord, "LGA": lga, "LAX": lax, "SFO": sfo}

def sample_schedule_2() -> dict[str, Airport]:
    """
    Returns: Sample schedule described in Task 4.
    """

    ord = Airport("Chicago O'Hare", "ORD")  # pylint: disable=redefined-builtin
    lga = Airport("New York LaGuardia", "LGA")
    sfo = Airport("San Francisco International", "SFO")

    ord.add_flight(Flight(ord, lga, "UC", 1001, TimeOfDay.MORNING, 200))
    lga.add_flight(Flight(lga, ord, "UC", 1002, TimeOfDay.AFTERNOON, 300))

    ord.add_flight(Flight(ord, sfo, "UC", 1003, TimeOfDay.MORNING, 5000))
    ord.add_flight(Flight(ord, sfo, "UC", 1004, TimeOfDay.EVENING, 100))

    return {"ORD": ord, "LGA": lga, "SFO": sfo}

def sample_schedule_3() -> dict[str, Airport]:
    """
    This is a more elaborate schedule with 10 airports that, at a high level,
    are connected like this:

                      MSP
                       |
                       |
        SEA --------- ORD---------  LGA
         |          /  | ╲          /|
         |        /    |  ╲        / |
        PDX     /      |   ╲      /  |
         |    /        |    ╲    /   |
         |  /          |     ╲  /    |
        SFO            |     ATL     |
         |             |    /  ╲     |
         |             |  /     ╲    |
        LAX --------- AUS        ╲   |
                                  ╲  |
                                   ╲ |
                                   MIA

    Except for ORD/MSP, every edge above means there are four flights
    connecting a pair of airports: a morning/afternoon pair of flights
    (going from one airport to another, and returning) and an evening/night
    pair of flights on the schedule.

    There is only one flight going from ORD to MSP at night.

    The cost of the flights have been tweaked in such a way that, if you want
    to get to MSP from ORD starting in the morning, you first have to go to
    LGA, MIA, ATL, AUS, back to ORD, and finally to MSP.
    """

    ord = Airport("Chicago O'Hare", "ORD")  # pylint: disable=redefined-builtin
    lga = Airport("New York LaGuardia", "LGA")
    sfo = Airport("San Francisco International", "SFO")
    lax = Airport("Los Angeles International", "LAX")
    atl = Airport("Hartsfield-Jackson Atlanta International", "ATL")
    aus = Airport("Austin-Bergstrom International", "AUS")
    mia = Airport("Miami International", "MIA")
    sea = Airport("Seattle-Tacoma International", "SEA")
    pdx = Airport("Portland International", "PDX")
    msp = Airport("Minneapolis–Saint Paul International", "MSP")

    ord.add_flight(Flight(ord, lga, "UC", 2010, TimeOfDay.MORNING, 200))
    lga.add_flight(Flight(lga, ord, "UC", 2101, TimeOfDay.AFTERNOON, 2000))
    ord.add_flight(Flight(ord, lga, "UC", 2012, TimeOfDay.EVENING, 200))
    lga.add_flight(Flight(lga, ord, "UC", 2103, TimeOfDay.NIGHT, 300))

    ord.add_flight(Flight(ord, atl, "UC", 2040, TimeOfDay.MORNING, 1000))
    atl.add_flight(Flight(atl, ord, "UC", 2401, TimeOfDay.AFTERNOON, 2000))
    ord.add_flight(Flight(ord, atl, "UC", 2042, TimeOfDay.EVENING, 500))
    atl.add_flight(Flight(atl, ord, "UC", 2403, TimeOfDay.NIGHT, 600))

    aus.add_flight(Flight(aus, ord, "UC", 2501, TimeOfDay.MORNING, 600))
    ord.add_flight(Flight(ord, aus, "UC", 2052, TimeOfDay.AFTERNOON, 2000))
    aus.add_flight(Flight(aus, ord, "UC", 2503, TimeOfDay.EVENING, 200))
    ord.add_flight(Flight(ord, aus, "UC", 2050, TimeOfDay.NIGHT, 500))

    ord.add_flight(Flight(ord, sea, "UC", 2070, TimeOfDay.MORNING, 1000))
    sea.add_flight(Flight(sea, ord, "UC", 2701, TimeOfDay.AFTERNOON, 2000))
    ord.add_flight(Flight(ord, sea, "UC", 2072, TimeOfDay.EVENING, 1000))
    sea.add_flight(Flight(sea, ord, "UC", 2703, TimeOfDay.NIGHT, 900))

    ord.add_flight(Flight(ord, sfo, "UC", 2020, TimeOfDay.MORNING, 1200))
    sfo.add_flight(Flight(sfo, ord, "UC", 2201, TimeOfDay.AFTERNOON, 1100))
    ord.add_flight(Flight(ord, sfo, "UC", 2022, TimeOfDay.EVENING, 1200))
    sfo.add_flight(Flight(sfo, ord, "UC", 2203, TimeOfDay.NIGHT, 1100))

    lax.add_flight(Flight(lax, sfo, "UC", 2320, TimeOfDay.MORNING, 200))
    sfo.add_flight(Flight(sfo, lax, "UC", 2231, TimeOfDay.AFTERNOON, 300))
    lax.add_flight(Flight(lax, sfo, "UC", 2322, TimeOfDay.EVENING, 200))
    sfo.add_flight(Flight(sfo, lax, "UC", 2233, TimeOfDay.NIGHT, 300))

    sfo.add_flight(Flight(sfo, pdx, "UC", 2280, TimeOfDay.MORNING, 300))
    pdx.add_flight(Flight(pdx, sfo, "UC", 2821, TimeOfDay.AFTERNOON, 400))
    sfo.add_flight(Flight(sfo, pdx, "UC", 2282, TimeOfDay.EVENING, 300))
    pdx.add_flight(Flight(pdx, sfo, "UC", 2823, TimeOfDay.NIGHT, 400))

    pdx.add_flight(Flight(pdx, sea, "UC", 2870, TimeOfDay.MORNING, 200))
    sea.add_flight(Flight(sea, pdx, "UC", 2781, TimeOfDay.AFTERNOON, 300))
    pdx.add_flight(Flight(pdx, sea, "UC", 2872, TimeOfDay.EVENING, 200))
    sea.add_flight(Flight(sea, pdx, "UC", 2783, TimeOfDay.NIGHT, 300))

    aus.add_flight(Flight(aus, lax, "UC", 2530, TimeOfDay.MORNING, 900))
    lax.add_flight(Flight(lax, aus, "UC", 2351, TimeOfDay.AFTERNOON, 800))
    aus.add_flight(Flight(aus, lax, "UC", 2532, TimeOfDay.EVENING, 900))
    lax.add_flight(Flight(lax, aus, "UC", 2353, TimeOfDay.NIGHT, 800))

    atl.add_flight(Flight(atl, aus, "UC", 2450, TimeOfDay.MORNING, 200))
    aus.add_flight(Flight(aus, atl, "UC", 2541, TimeOfDay.AFTERNOON, 300))
    atl.add_flight(Flight(atl, aus, "UC", 2452, TimeOfDay.EVENING, 400))
    aus.add_flight(Flight(aus, atl, "UC", 2543, TimeOfDay.NIGHT, 300))

    lga.add_flight(Flight(lga, atl, "UC", 2140, TimeOfDay.MORNING, 200))
    atl.add_flight(Flight(atl, lga, "UC", 2411, TimeOfDay.AFTERNOON, 400))
    lga.add_flight(Flight(lga, atl, "UC", 2142, TimeOfDay.EVENING, 1000))
    atl.add_flight(Flight(atl, lga, "UC", 2413, TimeOfDay.NIGHT, 400))

    mia.add_flight(Flight(mia, lga, "UC", 2610, TimeOfDay.MORNING, 600))
    lga.add_flight(Flight(lga, mia, "UC", 2161, TimeOfDay.AFTERNOON, 200))
    mia.add_flight(Flight(mia, lga, "UC", 2612, TimeOfDay.EVENING, 600))
    lga.add_flight(Flight(lga, mia, "UC", 2163, TimeOfDay.NIGHT, 700))

    mia.add_flight(Flight(mia, atl, "UC", 2640, TimeOfDay.MORNING, 200))
    atl.add_flight(Flight(atl, mia, "UC", 2461, TimeOfDay.AFTERNOON, 300))
    mia.add_flight(Flight(mia, atl, "UC", 2642, TimeOfDay.EVENING, 200))
    atl.add_flight(Flight(atl, mia, "UC", 2463, TimeOfDay.NIGHT, 300))

    ord.add_flight(Flight(ord, msp, "UC", 2093, TimeOfDay.NIGHT, 50))

    return {"ORD": ord, "LGA": lga, "SFO": sfo, "LAX": lax, "PDX": pdx,
            "SEA": sea, "AUS": aus, "ATL": atl, "MSP": msp, "MIA": mia}

def sample_schedule_4() -> dict[str, Airport]:
    """
    Returns: A sample "schedule" with airports but no flights.
    """

    ord = Airport("Chicago O'Hare", "ORD")  # pylint: disable=redefined-builtin
    lga = Airport("New York LaGuardia", "LGA")
    lax = Airport("Los Angeles International", "LAX")
    sfo = Airport("San Francisco International", "SFO")

    return {"ORD": ord, "LGA": lga, "LAX": lax, "SFO": sfo}
