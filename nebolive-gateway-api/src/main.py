from fastapi import Depends, FastAPI, Query
from pydantic import BaseModel

from nebolive_service import NeboliveService, get_nebolive_service
from report import generate_report
from shortest_sensor import calculate_shortest_sensor

app = FastAPI(docs_url='/docs', redoc_url='/redoc', openapi_url='/openapi.json')


class ResponseNestedSchema(BaseModel):
    text: str
    end_session: bool = True


class YandexStationResponse(BaseModel):
    response: ResponseNestedSchema
    version: str = '1.0'


@app.post('/station/v1/', response_model=YandexStationResponse)
async def station(
    city: str = Query(..., description='город'),
    nebolive: NeboliveService = Depends(get_nebolive_service),
):
    aqi = nebolive.average_aqi(city)
    return YandexStationResponse(
        response=ResponseNestedSchema(
            text=generate_report(aqi=aqi),
            end_session=True,
        )
    )


@app.post('/station/v2/', response_model=YandexStationResponse)
async def station(
    city_slug: str = Query(..., description='город'),
    lat: float = Query(..., description='широта'),
    lng: float = Query(..., description='долгота'),
    nebolive: NeboliveService = Depends(get_nebolive_service),
):
    sensors = nebolive.fetch_sensors(city_slug)
    sensor = calculate_shortest_sensor(sensors, lat, lng)
    aqi = sensor.instant.aqi if sensor is not None else nebolive.average_aqi(city_slug)

    return YandexStationResponse(
        response=ResponseNestedSchema(
            text=generate_report(aqi=aqi),
            end_session=True,
        )
    )
