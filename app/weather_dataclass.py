import dataclasses
import datetime


@dataclasses.dataclass
class CurrentWeather:
    time : str
    place : str
    weather : str
    real_temperature : int
    feels_like_temparature : int
    wind_speed : float

    def to_JSON(self) -> dict:
        return dataclasses.asdict(self)