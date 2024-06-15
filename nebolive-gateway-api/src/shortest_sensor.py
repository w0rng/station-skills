import math
from dataclasses import dataclass

from nebolive_service import NeboliveSensorResponse


@dataclass
class Position:
    lat: float
    lng: float


def calculate_shortest_sensor(
    sensors: list[NeboliveSensorResponse],
    lat: float,
    lng: float,
) -> NeboliveSensorResponse | None:
    min_distance: float = float('inf')
    shortest_sensor: NeboliveSensorResponse | None = None
    curr_pos = Position(lat=lat, lng=lng)

    for sensor in sensors:
        if sensor.lat is None or sensor.lng is None:
            continue
        sensor_pos = Position(lat=sensor.lat, lng=sensor.lng)
        dist = distance(curr_pos, sensor_pos)
        if dist >= min_distance:
            continue
        min_distance = dist
        shortest_sensor = sensor

    return shortest_sensor


def distance(p1: Position, p2: Position) -> float:
    square_lat = (p2.lat - p1.lat) ** 2
    square_lng = (p2.lng - p1.lng) ** 2
    return math.sqrt(square_lat + square_lng)
