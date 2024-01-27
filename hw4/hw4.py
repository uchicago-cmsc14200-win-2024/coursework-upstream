"""
CMSC 14200, Winter 2024
Homework #4

People Consulted:
   List anyone (other than the course staff) that you consulted about
   this assignment.

Online resources consulted:
   List the URLs of any online resources other than the course text and
   the official Python language documentation that you used to complete
   this assignment.
"""

import heapq
import csv
from typing import Optional

from flights import Airport, Flight, TimeOfDay

def valid_flights(airport: Airport, arrival_time: TimeOfDay) -> set[Flight]:
    """
    Given an airport, return all the flights departing from that
    airport that a passenger could take if they arrived to the airport
    at a given time.

    Args:
        airport: An airport
        arrival_time: Time of day when the passenger arrives at the airport-

    Returns: A set of flights

    """
    raise NotImplementedError

def process_itinerary(origin: Airport, start: TimeOfDay,
                      flight_codes: list[str]) -> Optional[Airport]:
    """
    Given an itinerary (as a list of flight codes), check whether
    it is a valid sequence of flights, assuming we start the itinerary
    at a given airport and at a given time.

    An itinerary is not valid if any of the following happens:

    - We are at an airport, and the next flight on the itinerary
      does not exist (i.e., there is no flight with that code in
      that airport)
    - The flight does exist, but taking it does not meet the layover
      rule.

    If the itinerary is valid, the function returns the final airport
    after taking all the flights. If the itinerary is not valid, the
    function returns None.

    Args:
        origin: The airport where we start the itinerary.
        start: The time of day at which we start the itinerary.
        flight_codes: The itinerary, as a list of flight codes.

    Returns: The Airport object for the final airport, if the itinerary
      is valid, otherwise returns None.
    """
    raise NotImplementedError

def is_reachable(origin: Airport, destination: Airport,
                 start: TimeOfDay) -> bool:
    """
    Given an origin and destination airport, determine whether there exists
    an itinerary that allows me to get from the origin to the destination
    (assuming I start the itinerary at a given time)

    We only care about whether such an itinerary exists or not. We do not
    need to compute the actual itinerary, nor do we care about whether
    it is the best possible itinerary.

    Args:
        origin, destination: Airports
        start: Time at which we start the itinerary

    Returns: True if I can reach the destination from the origin,
             False otherwise.
    """
    raise NotImplementedError

def best_itinerary(origin: Airport, destination: Airport, start: TimeOfDay) \
        -> Optional[tuple[int, list[Flight]]]:
    """
    Given an origin and destination airport, find the lowest-cost itinerary
    (as determined by the "cost" attribute of the flights) between the
    two airports, assuming we start the itinerary at a given time.

    Args:
        origin, destination: Airports
        start: Time at which we start the itinerary

    Returns: If there exists an itinerary between the two airports,
        return a tuple with the total cost of the itinerary, and a list
        of flights that make up the itinerary. Otherwise, return None.
    """

    raise NotImplementedError

def load_flights(flights_file_path: str) -> Optional[dict[str, Airport]]:
    """
    Given a CSV file containing flight information, load that information
    into a dictionary mapping airport codes to Airport objects containing
    the appropriate Flight objects.

    Args:
        flights_file_path: Path to file

    Returns: Dictionary of Airport objects if the file exists. None if
      no such file exists.
    """
    raise NotImplementedError
