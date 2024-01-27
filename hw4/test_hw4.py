"""
Tests for Homework #4
"""

import subprocess
import sys
from typing import Optional

import pytest

from flights import (Flight, TimeOfDay, sample_schedule_1, Airport,
                     sample_schedule_2, sample_schedule_3, sample_schedule_4)

from hw4 import (valid_flights, process_itinerary, is_reachable,
                 best_itinerary, load_flights)

#
# TASK 1 TESTS
#

def flight_str_list(flights: set[Flight]) -> str:
    """
    Returns: Newline-separated string representations of flights
    """
    return '\n'.join(str(f) for f in flights)


def validate_flights(airports: dict[str, Airport], airport_code: str,
                     time: TimeOfDay, expected_flight_codes: str) -> None:
    """
    Validates the valid flights of an airport at a given time of day.
    """
    actual = valid_flights(airports[airport_code], time)

    if expected_flight_codes == "NO-VALID-FLIGHTS":
        expected: set[Flight] = set()
    else:
        expected = set(airports[airport_code].get_flight_by_code(code) for code in expected_flight_codes.split(","))

    error_msg = "\n"
    if len(expected) == 0:
        error_msg += "Expected no flights, but got these instead:\n\n"
        error_msg += flight_str_list(actual)
    else:
        error_msg += "Expected the following set of flights:\n\n"
        error_msg += flight_str_list(expected)
        error_msg += "\n\n"
        if len(actual) == 0:
            error_msg += "\n\nbut got none instead."
        else:
            error_msg += "but got these instead:\n\n"
            error_msg += flight_str_list(actual)
    error_msg += "\n"

    assert expected == actual, error_msg

# Exhaustive list of valid flights in Schedule 1
schedule_1_outbound_flights = [("ORD", TimeOfDay.MORNING, "UC0001,UC0002"),
                               ("ORD", TimeOfDay.AFTERNOON, "UC0002"),
                               ("ORD", TimeOfDay.EVENING, "NO-VALID-FLIGHTS"),
                               ("ORD", TimeOfDay.NIGHT, "UC0001"),
                               ("LGA", TimeOfDay.MORNING, "UC0003,UC0004"),
                               ("LGA", TimeOfDay.AFTERNOON, "UC0004"),
                               ("LGA", TimeOfDay.EVENING, "NO-VALID-FLIGHTS"),
                               ("LGA", TimeOfDay.NIGHT, "UC0003"),
                               ("SFO", TimeOfDay.MORNING, "NO-VALID-FLIGHTS"),
                               ("SFO", TimeOfDay.AFTERNOON, "NO-VALID-FLIGHTS"),
                               ("SFO", TimeOfDay.EVENING, "UC0007"),
                               ("SFO", TimeOfDay.NIGHT, "UC0007"),
                               ("LAX", TimeOfDay.MORNING, "NO-VALID-FLIGHTS"),
                               ("LAX", TimeOfDay.AFTERNOON, "UC0006"),
                               ("LAX", TimeOfDay.EVENING, "UC0005,UC0006"),
                               ("LAX", TimeOfDay.NIGHT, "UC0005")]

# Exhaustive list of valid flights in Schedule 2
schedule_2_outbound_flights = [("ORD", TimeOfDay.MORNING, "UC1001,UC1003"),
                               ("ORD", TimeOfDay.AFTERNOON, "UC1004"),
                               ("ORD", TimeOfDay.EVENING, "UC1004"),
                               ("ORD", TimeOfDay.NIGHT, "UC1001,UC1003"),
                               ("LGA", TimeOfDay.MORNING, "UC1002"),
                               ("LGA", TimeOfDay.AFTERNOON, "UC1002"),
                               ("LGA", TimeOfDay.EVENING, "NO-VALID-FLIGHTS"),
                               ("LGA", TimeOfDay.NIGHT, "NO-VALID-FLIGHTS"),
                               ("SFO", TimeOfDay.MORNING, "NO-VALID-FLIGHTS"),
                               ("SFO", TimeOfDay.AFTERNOON, "NO-VALID-FLIGHTS"),
                               ("SFO", TimeOfDay.EVENING, "NO-VALID-FLIGHTS"),
                               ("SFO", TimeOfDay.NIGHT, "NO-VALID-FLIGHTS")]

@pytest.mark.parametrize("airport_code,time,expected_flight_codes",
                         schedule_1_outbound_flights)
def test_task1_1(airport_code: str, time: TimeOfDay, expected_flight_codes: str) -> None:
    """
    Checks the valid flights in Schedule 1
    """
    airports = sample_schedule_1()

    validate_flights(airports, airport_code, time, expected_flight_codes)


@pytest.mark.parametrize("airport_code,time,expected_flight_codes",
                         schedule_2_outbound_flights)
def test_task1_2(airport_code: str, time: TimeOfDay, expected_flight_codes: str) -> None:
    """
    Checks the valid flights in Schedule 2
    """
    airports = sample_schedule_2()

    validate_flights(airports, airport_code, time, expected_flight_codes)


def test_task1_no_flights() -> None:
    """
    Checks the valid flights in Schedule 4 (a schedule with airports but no flights)
    """

    airports = sample_schedule_4()

    for airport in airports.values():
        for time in (TimeOfDay.MORNING, TimeOfDay.AFTERNOON, TimeOfDay.EVENING, TimeOfDay.NIGHT):
            flights = valid_flights(airport, time)

            assert len(flights) == 0, f"sample_schedule_4() has no flights, yet valid_flights returned flights " \
                                      f"for {airport.code} at {time.name}"


#
# TASK 2 TESTS
#


def check_valid_itinerary(airports: dict[str, Airport], airport_code: str,
                          time: TimeOfDay, flight_codes: str, final_airport_code: str) -> None:
    """
    Checks that an itinerary is valid
    """
    origin = airports[airport_code]
    codes = flight_codes.split("/")

    final_airport = process_itinerary(origin, time, codes)

    if final_airport_code == "NOT-VALID":
        assert final_airport is None
    else:
        assert final_airport == airports[final_airport_code]

# Sampling of itineraries in Schedule 1
schedule_1_itineraries = [("ORD", TimeOfDay.MORNING, "UC0001/UC0004/UC0006", "SFO"),
                          ("LGA", TimeOfDay.MORNING, "UC0003/UC0005", "NOT-VALID"),
                          ("ORD", TimeOfDay.MORNING, "UC0001", "LGA"),
                          ("ORD", TimeOfDay.MORNING, "UC0002", "LGA"),
                          ("ORD", TimeOfDay.AFTERNOON, "UC0002", "LGA"),
                          ("ORD", TimeOfDay.MORNING, "UC0001/UC0004/UC0006/UC0007", "ORD"),
                          ("ORD", TimeOfDay.MORNING, "UC0001/UC0004/UC0005", "LGA"),
                          ("ORD", TimeOfDay.MORNING, "UC0001/UC0004/UC0005/UC0003", "LAX"),
                          ("LGA", TimeOfDay.AFTERNOON, "UC0004/UC0005", "LGA"),
                          ("LGA", TimeOfDay.MORNING, "UC0004/UC0005", "LGA"),
                          ("ORD", TimeOfDay.MORNING, "UC1234", "NOT-VALID"),
                          ("ORD", TimeOfDay.MORNING, "UC0001/UC1234/UC0005/UC0003", "NOT-VALID"),
                          ("ORD", TimeOfDay.AFTERNOON, "UC0002/UC0003", "NOT-VALID")]

# Sampling of itineraries in Schedule 2
schedule_2_itineraries = [("ORD", TimeOfDay.MORNING, "UC1001/UC1002/UC1004", "SFO"),
                          ("ORD", TimeOfDay.MORNING, "UC1001/UC1002", "ORD"),
                          ("ORD", TimeOfDay.MORNING, "UC1003", "SFO"),
                          ("ORD", TimeOfDay.AFTERNOON, "UC1001/UC1002/UC1004", "NOT-VALID"),
                          ("ORD", TimeOfDay.AFTERNOON, "UC1001/UC1002", "NOT-VALID"),
                          ("ORD", TimeOfDay.AFTERNOON, "UC1003", "NOT-VALID"),
                          ("LGA", TimeOfDay.AFTERNOON, "UC1002", "ORD"),
                          ("LGA", TimeOfDay.AFTERNOON, "UC1002/UC1004", "SFO"),
                          ("LGA", TimeOfDay.AFTERNOON, "UC1002/UC1003", "NOT-VALID")]

# Sampling of itineraries in Schedule 3
schedule_3_itineraries = [("AUS", TimeOfDay.NIGHT, "UC2530/UC2322/UC2233/UC2320/UC2231/UC2322/UC2203/UC2052/UC2503/UC2020", "SFO"),
                          ("ORD", TimeOfDay.AFTERNOON, "UC2022/UC2280/UC2821/UC2233/UC2351/UC2543/UC2450/UC2503/UC2010/UC2101", "ORD"),
                          ("SFO", TimeOfDay.MORNING, "UC2201/UC2050/UC2530/UC2351/UC2503/UC2040/UC2452/UC2530/UC2351/UC2543", "ATL"),
                          ("LAX", TimeOfDay.MORNING, "UC2351/UC2532/UC2353/UC2501/UC2072/UC2703/UC2020/UC2231/UC2353/UC2501", "ORD"),
                          ("SFO", TimeOfDay.NIGHT, "UC2203/UC2020/UC2231/UC2353/UC2541/UC2463/UC2610/UC2161/UC2642/UC2403", "ORD"),
                          ("SFO", TimeOfDay.NIGHT, "UC2280/UC2872/UC2703/UC2020/UC2282/UC2823/UC2280/UC2821/UC2203/UC2070", "SEA"),
                          ("ORD", TimeOfDay.EVENING, "UC2042/UC2413/UC2140/UC2452/UC2530/UC2322/UC2203/UC2070/UC2781/UC2823", "SFO"),
                          ("PDX", TimeOfDay.AFTERNOON, "UC2872/UC2703/UC2052/UC2503/UC2010/UC2101/UC2050/UC2501/UC2052/UC2503", "ORD"),
                          ("SFO", TimeOfDay.EVENING, "UC2203/UC2052/UC2503/UC2020/UC2282/UC2823/UC2201/UC2072/UC2703/UC2010", "LGA"),
                          ("SFO", TimeOfDay.MORNING, "UC2231/UC2322/UC2233/UC2320/UC2282/UC2823/UC2201/UC2093", "MSP"),
                          ("LGA", TimeOfDay.AFTERNOON, "UC2161/UC2642/UC2463/UC2640/UC2401/UC2010/UC2103/UC2070/UC2781/UC2823", "NOT-VALID"),
                          ("SEA", TimeOfDay.EVENING, "UC2703/UC2040/UC2401/UC2053/UC2541/UC2413/UC2140/UC2401/UC2022/UC2233", "NOT-VALID"),
                          ("LGA", TimeOfDay.AFTERNOON, "UC2101/UC2022/UC2233/UC2320/UC1234/UC2322/UC2233/UC2320/UC2231/UC2353", "NOT-VALID"),
                          ("MIA", TimeOfDay.MORNING, "UC2640/UC2461/XX0000/UC2163/UC2640/UC2452/UC2543/UC2411/UC2163/UC2610", "NOT-VALID"),
                          ("AUS", TimeOfDay.NIGHT, "UC2543/UC2450/UC2503/UC2040/UC2461/UC2612/UC2140/UC2460/UC2642/UC2413", "NOT-VALID")
                          ]

@pytest.mark.parametrize("airport_code,time,flight_codes,final_airport",
                         schedule_1_itineraries)
def test_task2_1(airport_code: str, time: TimeOfDay, flight_codes: str, final_airport: str) -> None:
    """
    Checks valid itineraries in Schedule 1
    """
    airports = sample_schedule_1()

    check_valid_itinerary(airports, airport_code, time, flight_codes, final_airport)

@pytest.mark.parametrize("airport_code,time,flight_codes,final_airport",
                         schedule_2_itineraries)
def test_task2_2(airport_code: str, time: TimeOfDay, flight_codes: str, final_airport: str) -> None:
    """
    Checks valid itineraries in Schedule 2
    """
    airports = sample_schedule_2()

    check_valid_itinerary(airports, airport_code, time, flight_codes, final_airport)

@pytest.mark.parametrize("airport_code,time,flight_codes,final_airport",
                         schedule_3_itineraries)
def test_task2_3(airport_code: str, time: TimeOfDay, flight_codes: str, final_airport: str) -> None:
    """
    Checks valid itineraries in Schedule 3
    """
    airports = sample_schedule_3()

    check_valid_itinerary(airports, airport_code, time, flight_codes, final_airport)


#
# TASK 3 TEST
#


def check_reachable(schedule: str, airports: dict[str, Airport], origin: str,
                    destination: str, time: TimeOfDay, expected: bool) -> None:
    """
    Checks reachability of one airport from another at a given time of day
    """

    actual = is_reachable(airports[origin], airports[destination], time)
    not_str = "not " if expected is False else ""

    assert actual == expected, f"In sample schedule {schedule}, expected {destination} " \
            f"to {not_str}be reachable from {origin} starting at {time.name}, but is_reachable returned {actual}"


# Exhaustive list of reachable pairs in Schedule 1
schedule_1_reachability = [("ORD", "ORD", TimeOfDay.MORNING, True),
                           ("ORD", "ORD", TimeOfDay.AFTERNOON, True),
                           ("ORD", "ORD", TimeOfDay.EVENING, True),
                           ("ORD", "ORD", TimeOfDay.NIGHT, True),
                           ("ORD", "LGA", TimeOfDay.MORNING, True),
                           ("ORD", "LGA", TimeOfDay.AFTERNOON, True),
                           ("ORD", "LGA", TimeOfDay.EVENING, False),
                           ("ORD", "LGA", TimeOfDay.NIGHT, True),
                           ("ORD", "SFO", TimeOfDay.MORNING, True),
                           ("ORD", "SFO", TimeOfDay.AFTERNOON, False),
                           ("ORD", "SFO", TimeOfDay.EVENING, False),
                           ("ORD", "SFO", TimeOfDay.NIGHT, True),
                           ("ORD", "LAX", TimeOfDay.MORNING, True),
                           ("ORD", "LAX", TimeOfDay.AFTERNOON, False),
                           ("ORD", "LAX", TimeOfDay.EVENING, False),
                           ("ORD", "LAX", TimeOfDay.NIGHT, True),

                           ("LGA", "ORD", TimeOfDay.MORNING, True),
                           ("LGA", "ORD", TimeOfDay.AFTERNOON, True),
                           ("LGA", "ORD", TimeOfDay.EVENING, False),
                           ("LGA", "ORD", TimeOfDay.NIGHT, True),
                           ("LGA", "LGA", TimeOfDay.MORNING, True),
                           ("LGA", "LGA", TimeOfDay.AFTERNOON, True),
                           ("LGA", "LGA", TimeOfDay.EVENING, True),
                           ("LGA", "LGA", TimeOfDay.NIGHT, True),
                           ("LGA", "SFO", TimeOfDay.MORNING, True),
                           ("LGA", "SFO", TimeOfDay.AFTERNOON, True),
                           ("LGA", "SFO", TimeOfDay.EVENING, False),
                           ("LGA", "SFO", TimeOfDay.NIGHT, True),
                           ("LGA", "LAX", TimeOfDay.MORNING, True),
                           ("LGA", "LAX", TimeOfDay.AFTERNOON, True),
                           ("LGA", "LAX", TimeOfDay.EVENING, False),
                           ("LGA", "LAX", TimeOfDay.NIGHT, True),

                           ("SFO", "LGA", TimeOfDay.MORNING, False),
                           ("SFO", "LGA", TimeOfDay.AFTERNOON, False),
                           ("SFO", "LGA", TimeOfDay.EVENING, True),
                           ("SFO", "LGA", TimeOfDay.NIGHT, True),
                           ("SFO", "ORD", TimeOfDay.MORNING, False),
                           ("SFO", "ORD", TimeOfDay.AFTERNOON, False),
                           ("SFO", "ORD", TimeOfDay.EVENING, True),
                           ("SFO", "ORD", TimeOfDay.NIGHT, True),
                           ("SFO", "SFO", TimeOfDay.MORNING, True),
                           ("SFO", "SFO", TimeOfDay.AFTERNOON, True),
                           ("SFO", "SFO", TimeOfDay.EVENING, True),
                           ("SFO", "SFO", TimeOfDay.NIGHT, True),
                           ("SFO", "LAX", TimeOfDay.MORNING, False),
                           ("SFO", "LAX", TimeOfDay.AFTERNOON, False),
                           ("SFO", "LAX", TimeOfDay.EVENING, True),
                           ("SFO", "LAX", TimeOfDay.NIGHT, True),

                           ("LAX", "LGA", TimeOfDay.MORNING, False),
                           ("LAX", "LGA", TimeOfDay.AFTERNOON, True),
                           ("LAX", "LGA", TimeOfDay.EVENING, True),
                           ("LAX", "LGA", TimeOfDay.NIGHT, True),
                           ("LAX", "SFO", TimeOfDay.MORNING, False),
                           ("LAX", "SFO", TimeOfDay.AFTERNOON, True),
                           ("LAX", "SFO", TimeOfDay.EVENING, True),
                           ("LAX", "SFO", TimeOfDay.NIGHT, True),
                           ("LAX", "LAX", TimeOfDay.MORNING, True),
                           ("LAX", "LAX", TimeOfDay.AFTERNOON, True),
                           ("LAX", "LAX", TimeOfDay.EVENING, True),
                           ("LAX", "LAX", TimeOfDay.NIGHT, True),
                           ("LAX", "ORD", TimeOfDay.MORNING, False),
                           ("LAX", "ORD", TimeOfDay.AFTERNOON, True),
                           ("LAX", "ORD", TimeOfDay.EVENING, True),
                           ("LAX", "ORD", TimeOfDay.NIGHT, True)]

# Exhaustive list of reachable pairs in Schedule 2
schedule_2_reachability = [("ORD", "LGA", TimeOfDay.MORNING, True),
                           ("ORD", "LGA", TimeOfDay.AFTERNOON, False),
                           ("ORD", "LGA", TimeOfDay.EVENING, False),
                           ("ORD", "LGA", TimeOfDay.NIGHT, True),
                           ("ORD", "ORD", TimeOfDay.MORNING, True),
                           ("ORD", "ORD", TimeOfDay.AFTERNOON, True),
                           ("ORD", "ORD", TimeOfDay.EVENING, True),
                           ("ORD", "ORD", TimeOfDay.NIGHT, True),
                           ("ORD", "SFO", TimeOfDay.MORNING, True),
                           ("ORD", "SFO", TimeOfDay.AFTERNOON, True),
                           ("ORD", "SFO", TimeOfDay.EVENING, True),
                           ("ORD", "SFO", TimeOfDay.NIGHT, True),

                           ("LGA", "ORD", TimeOfDay.MORNING, True),
                           ("LGA", "ORD", TimeOfDay.AFTERNOON, True),
                           ("LGA", "ORD", TimeOfDay.EVENING, False),
                           ("LGA", "ORD", TimeOfDay.NIGHT, False),
                           ("LGA", "LGA", TimeOfDay.MORNING, True),
                           ("LGA", "LGA", TimeOfDay.AFTERNOON, True),
                           ("LGA", "LGA", TimeOfDay.EVENING, True),
                           ("LGA", "LGA", TimeOfDay.NIGHT, True),
                           ("LGA", "SFO", TimeOfDay.MORNING, True),
                           ("LGA", "SFO", TimeOfDay.AFTERNOON, True),
                           ("LGA", "SFO", TimeOfDay.EVENING, False),
                           ("LGA", "SFO", TimeOfDay.NIGHT, False),

                           ("SFO", "LGA", TimeOfDay.MORNING, False),
                           ("SFO", "LGA", TimeOfDay.AFTERNOON, False),
                           ("SFO", "LGA", TimeOfDay.EVENING, False),
                           ("SFO", "LGA", TimeOfDay.NIGHT, False),
                           ("SFO", "SFO", TimeOfDay.MORNING, True),
                           ("SFO", "SFO", TimeOfDay.AFTERNOON, True),
                           ("SFO", "SFO", TimeOfDay.EVENING, True),
                           ("SFO", "SFO", TimeOfDay.NIGHT, True),
                           ("SFO", "ORD", TimeOfDay.MORNING, False),
                           ("SFO", "ORD", TimeOfDay.AFTERNOON, False),
                           ("SFO", "ORD", TimeOfDay.EVENING, False),
                           ("SFO", "ORD", TimeOfDay.NIGHT, False)]

# Sampling of reachable pairs in Schedule 3
schedule_3_reachability = [("ATL", "AUS", TimeOfDay.EVENING, True),
                           ("ATL", "AUS", TimeOfDay.NIGHT, True),
                           ("AUS", "MIA", TimeOfDay.EVENING, True),
                           ("LAX", "ORD", TimeOfDay.MORNING, True),
                           ("LGA", "ORD", TimeOfDay.AFTERNOON, True),
                           ("LGA", "ORD", TimeOfDay.NIGHT, True),
                           ("LGA", "SFO", TimeOfDay.EVENING, True),
                           ("ORD", "AUS", TimeOfDay.MORNING, True),
                           ("ORD", "LAX", TimeOfDay.NIGHT, True),
                           ("ORD", "MSP", TimeOfDay.AFTERNOON, True),
                           ("ORD", "SEA", TimeOfDay.AFTERNOON, True),
                           ("PDX", "LGA", TimeOfDay.NIGHT, True),
                           ("PDX", "MSP", TimeOfDay.MORNING, True),
                           ("PDX", "ORD", TimeOfDay.NIGHT, True),
                           ("PDX", "ORD", TimeOfDay.NIGHT, True),
                           ("SEA", "ATL", TimeOfDay.AFTERNOON, True),
                           ("SEA", "ATL", TimeOfDay.EVENING, True),
                           ("SEA", "ATL", TimeOfDay.NIGHT, True),
                           ("SEA", "LGA", TimeOfDay.NIGHT, True),
                           ("SEA", "SFO", TimeOfDay.NIGHT, True)]

@pytest.mark.parametrize("origin,destination,time, expected",
                         schedule_1_reachability)
def test_task3_1(origin: str, destination: str, time: TimeOfDay, expected: bool) -> None:
    """
    Checks the reachability of pairs of airports in Schedule 1
    """
    airports = sample_schedule_1()

    check_reachable("1", airports, origin, destination, time, expected)

@pytest.mark.parametrize("origin,destination,time, expected",
                         schedule_2_reachability)
def test_task3_2(origin: str, destination: str, time: TimeOfDay, expected: bool) -> None:
    """
    Checks the reachability of pairs of airports in Schedule 2
    """
    airports = sample_schedule_2()

    check_reachable("2", airports, origin, destination, time, expected)

@pytest.mark.parametrize("origin,destination,time, expected",
                         schedule_3_reachability)
def test_task3_3(origin: str, destination: str, time: TimeOfDay, expected: bool) -> None:
    """
    Checks the reachability of pairs of airports in Schedule 3
    """
    airports = sample_schedule_3()

    check_reachable("3", airports, origin, destination, time, expected)

def test_task3_3_msp() -> None:
    """
    Checks the reachability from MSP to other airports in Schedule 3
    (MSP has a single inboud flight; you cannot reach other airports
    from MSP, other than MSP itself)
    """

    airports = sample_schedule_3()

    for airport in airports:
        for time in range(0, 3):
            check_reachable("3", airports, "MSP", airport, TimeOfDay(time),
                            True if airport == "MSP" else False)

def test_task3_4() -> None:
    """
    Checks the reachability of pairs of airports in Schedule 4
    (a schedule with airports but no flights)
    """
    airports = sample_schedule_4()

    for airport1 in airports:
        for airport2 in airports:
            for time in range(0, 3):
                check_reachable("4", airports, airport1, airport2,
                                TimeOfDay(time), True if airport1 == airport2 else False)


#
# TASK 4 TESTS
#


def test_task4_1() -> None:
    """
    Schedule 1: Find the best itinerary from ORD to SFO starting in the morning
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["ORD"], airports["SFO"], TimeOfDay.MORNING)
    assert rv is not None

    cost, flights = rv
    assert cost == 600
    assert flights == [airports["ORD"].get_flight_by_code("UC0001"),
                       airports["LGA"].get_flight_by_code("UC0004"),
                       airports["LAX"].get_flight_by_code("UC0006")]

def test_task4_2() -> None:
    """
    Schedule 1: Find the best itinerary from ORD to LGA starting in the morning
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["ORD"], airports["LGA"], TimeOfDay.MORNING)
    assert rv is not None

    cost, flights = rv
    assert cost == 100
    assert flights == [airports["ORD"].get_flight_by_code("UC0002")]

def test_task4_3() -> None:
    """
    Schedule 1: Find the best itinerary from ORD to SFO starting at night
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["ORD"], airports["SFO"], TimeOfDay.NIGHT)
    assert rv is not None

    cost, flights = rv
    assert cost == 600
    assert flights == [airports["ORD"].get_flight_by_code("UC0001"),
                       airports["LGA"].get_flight_by_code("UC0004"),
                       airports["LAX"].get_flight_by_code("UC0006")]

def test_task4_4() -> None:
    """
    Schedule 1: Find the best itinerary from LAX to LGA starting in the evening
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["LAX"], airports["LGA"], TimeOfDay.EVENING)
    assert rv is not None

    cost, flights = rv
    assert cost == 550
    assert flights == [airports["LAX"].get_flight_by_code("UC0006"),
                       airports["SFO"].get_flight_by_code("UC0007"),
                       airports["ORD"].get_flight_by_code("UC0002")]

def test_task4_5() -> None:
    """
    Schedule 2: Find the best itinerary from ORD to SFO starting in the morning.

    Note that this will involve going to LGA, and then back to ORD to catch
    the cheaper flight to SFO.
    """
    airports = sample_schedule_2()

    rv = best_itinerary(airports["ORD"], airports["SFO"], TimeOfDay.MORNING)
    assert rv is not None

    cost, flights = rv
    assert cost == 600
    assert flights == [airports["ORD"].get_flight_by_code("UC1001"),
                       airports["LGA"].get_flight_by_code("UC1002"),
                       airports["ORD"].get_flight_by_code("UC1004")]

def test_task4_6() -> None:
    """
    Schedule 2: Find the best itinerary from LGA to SFO starting in the morning.
    """
    airports = sample_schedule_2()

    rv = best_itinerary(airports["LGA"], airports["SFO"], TimeOfDay.MORNING)
    assert rv is not None

    cost, flights = rv
    assert cost == 400
    assert flights == [airports["LGA"].get_flight_by_code("UC1002"),
                       airports["ORD"].get_flight_by_code("UC1004")]

def test_task4_7() -> None:
    """
    Schedule 2: Find the best itinerary from ORD to MSP starting in the morning.

    See the docstring for sample_schedule_3 for more details on this itinerary.
    """
    airports = sample_schedule_3()

    rv = best_itinerary(airports["ORD"], airports["MSP"], TimeOfDay.MORNING)
    assert rv is not None

    cost, flights = rv
    assert cost == 1050
    assert flights == [airports["ORD"].get_flight_by_code("UC2010"),
                       airports["LGA"].get_flight_by_code("UC2161"),
                       airports["MIA"].get_flight_by_code("UC2642"),
                       airports["ATL"].get_flight_by_code("UC2450"),
                       airports["AUS"].get_flight_by_code("UC2503"),
                       airports["ORD"].get_flight_by_code("UC2093"),
                       ]

def test_task4_not_reachable_1() -> None:
    """
    Schedule 1: Try to find the best itinerary from ORD to LGA
    starting in the evening (there is no such itinerary).
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["ORD"], airports["LGA"], TimeOfDay.EVENING)
    assert rv is None

def test_task4_not_reachable_2() -> None:
    """
    Schedule 1: Try to find the best itinerary from ORD to SFO
    starting in the afternoon (there is no such itinerary).
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["ORD"], airports["SFO"], TimeOfDay.AFTERNOON)
    assert rv is None

def test_task4_not_reachable_3() -> None:
    """
    Schedule 1: Try to find the best itinerary from LAX to SFO
    starting in the morning (there is no such itinerary).
    """
    airports = sample_schedule_1()

    rv = best_itinerary(airports["LAX"], airports["SFO"], TimeOfDay.MORNING)
    assert rv is None

def test_task4_not_reachable_4() -> None:
    """
    Schedule 1: Try to find the best itinerary from SFO to LGA
    starting in the morning (there is no such itinerary).
    """
    airports = sample_schedule_2()

    rv = best_itinerary(airports["SFO"], airports["LGA"], TimeOfDay.MORNING)
    assert rv is None

def test_task4_not_reachable_5() -> None:
    """
    Schedule 3: Try to find the best itinerary from MSP to MIA
    starting in the morning (there is no such itinerary).
    """
    airports = sample_schedule_3()

    rv = best_itinerary(airports["MSP"], airports["MIA"], TimeOfDay.MORNING)
    assert rv is None


#
# TASK 5
#

def compare_schedules(expected: dict[str, Airport], actual: dict[str, Airport]) -> None:
    """
    Compare two schedules to see if they are the same.
    """
    # Compare dictionary keys
    assert set(expected.keys()) == set(actual.keys())

    for airport_code in expected:
        # Compare attributes
        expected_airport = expected[airport_code]
        actual_airport = actual[airport_code]

        assert expected_airport.code == actual_airport.code
        assert expected_airport.name == actual_airport.name

        # Compare number of flights
        n_flights_expected = len(expected_airport.flights)
        n_flights_actual = len(actual_airport.flights)

        assert n_flights_expected == n_flights_actual, \
            f"Expected airport {expected_airport.code} to have {n_flights_expected} flights, " \
            f"but it has {n_flights_actual}"

        # Compare flight codes
        flight_codes_expected = set(f.code for f in expected_airport.flights)
        flight_codes_actual = set(f.code for f in actual_airport.flights)

        assert flight_codes_expected == flight_codes_actual, \
            f"Wrong flight codes in airport {expected_airport.code}"

        # Compare flight information
        for flight_code in flight_codes_expected:
            expected_flight = expected_airport.get_flight_by_code(flight_code)
            actual_flight = actual_airport.get_flight_by_code(flight_code)

            expected_origin = actual[expected_flight.origin.code]
            actual_origin = actual_flight.origin

            assert expected_origin == actual_origin, \
                f"Wrong origin in flight {flight_code}"

            expected_destination = actual[expected_flight.destination.code]
            actual_destination = actual_flight.destination

            assert expected_destination == actual_destination, \
                f"Wrong destination in flight {flight_code}"

            assert expected_flight.airline == actual_flight.airline, \
                f"Wrong airline in flight {flight_code}"

            assert expected_flight.flight_num == actual_flight.flight_num, \
                f"Wrong flight number in flight {flight_code}"

            assert expected_flight.departure_time == actual_flight.departure_time, \
                f"Wrong departure time in flight {flight_code}"

            assert expected_flight.cost == actual_flight.cost, \
                f"Wrong cost in flight {flight_code}"


def test_task5_sample_schedule_1() -> None:
    """
    Load sample schedule 1
    """
    expected = sample_schedule_1()

    actual = load_flights("files/sample-1.csv")
    assert actual is not None

    compare_schedules(expected, actual)

def test_task5_sample_schedule_2() -> None:
    """
    Load sample schedule 2
    """
    expected = sample_schedule_2()

    actual = load_flights("files/sample-2.csv")
    assert actual is not None

    compare_schedules(expected, actual)

def test_task5_sample_schedule_3() -> None:
    """
    Load sample schedule 3
    """
    expected = sample_schedule_3()

    actual = load_flights("files/sample-3.csv")
    assert actual is not None

    compare_schedules(expected, actual)

def test_task5_incorrect_file() -> None:
    """
    Try loading non-existent schedule files
    """
    for i in range(4, 20):
        filename = f"files/sample-{i}.csv"

        rv = load_flights(filename)

        assert rv is None, f"Called load_flights with an invalid filename ({filename})" \
                           f"Expected to get None, but instead got {rv}"


#
# TASK 6 TESTS
#

def tui_helper(schedule_name:str, commands: list[str], expected_outputs: list[str]) -> str:
    """
    Runs the TUI, runs one or more commands, and checks that the outputs are as expected.
    """

    schedule_file = f"files/{schedule_name}.csv"

    commands.append("EXIT")
    commands_bytes = bytes("\n".join(commands), encoding="utf-8")
    command = [sys.executable, "tui.py", schedule_file]

    try:
        proc = subprocess.run(command, input=commands_bytes, capture_output=True,
                              timeout=1, check=False)
    except subprocess.TimeoutExpired:
        pytest.fail("tui.py the program did not exit after the EXIT command.")

    stdout = proc.stdout.decode(encoding="utf-8")
    stderr = proc.stderr.decode(encoding="utf-8")

    if proc.returncode != 0:
        pytest.fail(f"tui.py crashed when running:\n\n{stdout}\n{stderr}")

    for output in expected_outputs:
        assert output in stdout, \
            f"\nExpected the tui.py to print this\n\n{output}\n\n" \
            f"But it did not do so.\nThe actual output was the following:\n" \
            f"(this does not include commands)\n\n{stdout}"

    return stdout

def test_task6_opening_message() -> None:
    """
    Check that the TUI prints the correct start message
    """
    stdout = tui_helper("sample-1", [], [])
    msg = "WELCOME TO THE TRAVEL AGENT 3000"

    assert stdout.startswith(msg), \
        f"The TUI must print the following message on startup:\n\n{msg}"

def test_task6_prompt() -> None:
    """
    Check that the TUI prints a prompt (the ">" character)
    """
    stdout = tui_helper("sample-1", [], [])

    assert ">" in stdout, \
        "The TUI must print out a prompt with character '>'"

@pytest.mark.parametrize("airport_code", ["ORD", "LGA", "LAX", "SFO"])
def test_task6_outbound_flights_1(airport_code: str) -> None:
    """
    Run the outbound flights command for every airport in Schedule 1
    """
    airports = sample_schedule_1()

    expected = [str(f) for f in airports[airport_code].flights]

    tui_helper("sample-1", [airport_code+"?"], expected)

def check_tui_valid_itinerary(schedule_file:str, command: str, expected_airport: Optional[Airport]) -> None:
    """
    Check the output of the valid itinerary command
    """
    if expected_airport is None:
        expected_output = "NOT VALID"
    else:
        expected_output = f"{expected_airport.name} ({expected_airport.code})"

    tui_helper(schedule_file, [command], [expected_output])

def test_task6_valid_itinerary_1() -> None:
    """
    Schedule 1: ORD UC0001/UC0004/UC0006 @MORNING
    """
    airports = sample_schedule_1()

    check_tui_valid_itinerary("sample-1", "ORD UC0001/UC0004/UC0006 @MORNING", airports["SFO"])

def test_task6_valid_itinerary_2() -> None:
    """
    Schedule 1: ORD UC0001/UC0004/UC0005 @MORNING
    """
    airports = sample_schedule_1()

    check_tui_valid_itinerary("sample-1", "ORD UC0001/UC0004/UC0005 @MORNING", airports["LGA"])

def test_task6_valid_itinerary_3() -> None:
    """
    Schedule 1: LGA UC0003/UC0005 @MORNING
    """
    check_tui_valid_itinerary("sample-1", "LGA UC0003/UC0005 @MORNING", None)

def test_task6_valid_itinerary_4() -> None:
    """
    Schedule 1: ORD UC0002/UC0003 @AFTERNOON
    """
    check_tui_valid_itinerary("sample-1", "ORD UC0002/UC0003 @AFTERNOON", None)


def check_tui_reachable(schedule_file:str, command: str, reachable: bool) -> None:
    """
    Checks the output of the reachable command
    """
    if reachable:
        expected_output = "OK"
    else:
        expected_output = "REACHABLE"

    tui_helper(schedule_file, [command], [expected_output])

def test_task6_reachable_1() -> None:
    """
    Schedule 1: ORD??LGA @MORNING
    """
    check_tui_reachable("sample-1", "ORD??LGA @MORNING", True)

def test_task6_reachable_2() -> None:
    """
    Schedule 1: ORD??SFO @MORNING
    """
    check_tui_reachable("sample-1", "ORD??SFO @MORNING", True)

def test_task6_reachable_3() -> None:
    """
    Schedule 1: LAX??SFO @NIGHT
    """
    check_tui_reachable("sample-1", "LAX??SFO @NIGHT", True)

def test_task6_reachable_4() -> None:
    """
    Schedule 1: ORD??LGA @EVENING
    """
    check_tui_reachable("sample-1", "ORD??LGA @EVENING", False)

def test_task6_reachable_5() -> None:
    """
    Schedule 1: ORD??SFO @AFTERNOON
    """
    check_tui_reachable("sample-1", "ORD??SFO @AFTERNOON", False)

def test_task6_reachable_6() -> None:
    """
    Schedule 1: LAX??SFO @MORNING
    """
    check_tui_reachable("sample-1", "LAX??SFO @MORNING", False)

def check_tui_best_itinerary(schedule_file:str, command: str,
                             expected_flights: Optional[list[Flight]],
                             expected_cost: Optional[int]) -> None:
    """
    Checks the output of the best itinerary command
    """
    if expected_flights is None:
        expected_output = "NOT FEASIBLE"
    else:
        assert expected_cost is not None
        expected_output = "\n".join([str(f) for f in expected_flights] + [f"TOTAL: ${expected_cost}"])

    tui_helper(schedule_file, [command], [expected_output])

def test_task6_best_itinerary_1() -> None:
    """
    Schedule 1: ORD>>SFO @MORNING
    """
    airports = sample_schedule_1()
    expected_flights = [airports["ORD"].get_flight_by_code("UC0001"),
                       airports["LGA"].get_flight_by_code("UC0004"),
                       airports["LAX"].get_flight_by_code("UC0006")]
    expected_cost = 600

    check_tui_best_itinerary("sample-1", "ORD>>SFO @MORNING",
                              expected_flights, expected_cost)

def test_task6_best_itinerary_2() -> None:
    """
    Schedule 1: LAX>>LGA @EVENING
    """
    airports = sample_schedule_1()
    expected_flights = [airports["LAX"].get_flight_by_code("UC0006"),
                       airports["SFO"].get_flight_by_code("UC0007"),
                       airports["ORD"].get_flight_by_code("UC0002")]
    expected_cost = 550

    check_tui_best_itinerary("sample-1", "LAX>>LGA @EVENING",
                              expected_flights, expected_cost)

def test_task6_best_itinerary_3() -> None:
    """
    Schedule 1: ORD>>LGA @EVENING
    """
    check_tui_best_itinerary("sample-1", "ORD>>LGA @EVENING", None, None)

def test_task6_best_itinerary_4() -> None:
    """
    Schedule 1: ORD>>SFO @AFTERNOON
    """
    check_tui_best_itinerary("sample-1", "ORD>>SFO @AFTERNOON", None, None)

def test_task6_best_itinerary_5() -> None:
    """
    Schedule 1: LAX>>SFO @MORNING
    """
    check_tui_best_itinerary("sample-1", "LAX>>SFO @MORNING", None, None)

def test_task6_multiple_commands_1() -> None:
    """
    Tries running multiple commands
    """
    airports = sample_schedule_1()

    commands = ["ORD?",
                "ORD UC0001/UC0004/UC0005 @MORNING",
                "ORD??SFO @MORNING"
                ]

    expected_output = [str(f) for f in airports["ORD"].flights]
    expected_output += [f"{airports['LGA'].name} ({airports['LGA'].code})"]
    expected_output += ["OK"]

    tui_helper("sample-1", commands, expected_output)


@pytest.mark.parametrize("command", ["MDW?",
                                     "ORD??",
                                     "FOOBAR?",
                                     "MDW UC0001/UC0003 @MORNING",
                                     "ORD UC0001/UC0003 @LUNCHTIME",
                                     "ORD??MDW @MORNING",
                                     "OHare??LaGuardia @MORNING",
                                     "ORD??LGA??LAX @MORNING",
                                     "ORD??LGA @TEATIME",
                                     "MDW>>ORD @MORNING",
                                     "OHare>>LaGuardia @MORNING",
                                     "ORD>>LGA>>LAX @MORNING",
                                     "ORD>>LGA @SUPPERTIME",
                                     "Hello!",
                                     "Can you book me a ticket?"
                                     ])
def test_task6_invalid_command(command: str) -> None:
    """
    Tries running several invalid commands
    """
    tui_helper("sample-1", [command], ["Error"])
