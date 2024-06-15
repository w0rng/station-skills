import hashlib
import logging
import time
from os import environ

import requests
from bs4 import BeautifulSoup
from pydantic import UUID4, BaseModel, TypeAdapter
from starlette import status

logger = logging.getLogger(__name__)


class SensorData(BaseModel):
    aqi: int


class NeboliveSensorResponse(BaseModel):
    id: UUID4
    lat: float | None
    lng: float | None
    instant: SensorData


NeboliveSensors = TypeAdapter(list[NeboliveSensorResponse])


class NeboliveService:
    def __init__(self, token: str, code: str):
        self._token = token
        self._code = code

    def average_aqi(self, city: str) -> int | None:
        response = requests.get(f'https://nebo.live/ru/{city}/')
        if response.status_code != status.HTTP_200_OK:
            return None
        return self._parse_aqi(response.text)

    def fetch_sensors(self, city_slug: str) -> list[NeboliveSensorResponse]:
        """Список датчиков."""
        url = f'https://nebo.live/api/v2/cities/{city_slug}/'
        response = requests.get(url, params=self.query_params, headers=self._headers)
        if response.status_code != status.HTTP_200_OK:
            logger.warning(f'city_{city_slug}, status code: {response.status_code}, response: {response.text}')
            return []

        sensors = NeboliveSensors.validate_python(response.json())
        return sensors

    def fetch_sensor_aqi(self, sensor_id: UUID4) -> int | None:
        """Показание aqi датчика."""
        url = f'https://nebo.live/api/v2/sensors/{sensor_id}/'
        response = requests.get(url, params=self.query_params, headers=self._headers)
        if response.status_code != status.HTTP_200_OK:
            logger.warning(f'sensor_{sensor_id}, status code: {response.status_code}, response: {response.text}')
            return None

        sensor_data = NeboliveSensorResponse.model_validate(response.json())
        return sensor_data.instant.aqi

    @property
    def query_params(self) -> dict[str, str]:
        timestamp = int(time.time())
        concat = f'{timestamp}{self._code}'
        full_hash = hashlib.sha1(concat.encode()).hexdigest()
        minimal_hash = full_hash[5:16]
        return {
            'time': timestamp,
            'hash': minimal_hash,
        }

    @property
    def _headers(self) -> dict[str, str]:
        return {'X-Auth-Nebo': self._token}

    @staticmethod
    def _parse_aqi(content_page: str) -> int | None:
        soup = BeautifulSoup(content_page, 'html.parser')
        res = soup.find('meta', {'name': 'description'})
        sentence: list[str] = res.get('content').split()
        aqi = sentence[-1].replace('(', '').replace(')', '').replace('.', '')
        if not aqi.isdigit():
            return None
        return int(aqi)


def get_nebolive_service() -> NeboliveService:
    return NeboliveService(environ['NEBOLIVE_TOKEN'], environ['NEBOLIVE_CODE'])
