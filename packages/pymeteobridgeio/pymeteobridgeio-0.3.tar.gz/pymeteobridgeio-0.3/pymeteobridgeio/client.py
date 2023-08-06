"""Wrapper to retrieve Sensor data from a Meteobridge Data Logger
   Specifically developed to wotk with Home Assistant
   Developed by: @briis
   Github: https://github.com/briis/pymeteobridgeio
   License: MIT
"""

import csv
import aiohttp

import logging
from datetime import datetime
from pymeteobridgeio.dataclasses import HomeAssistantBinarySensors, HomeAssistantData
from pymeteobridgeio.const import (
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_RAIN,
    DEVICE_CLASS_RAINRATE,
    DEVICE_CLASS_WIND,
    DEVICE_CLASS_WIND_DIRECTION,
    DEVICE_CLASS_NONE,
    ENTITY_TYPE_SENSOR,
    ENTITY_TYPE_BINARY_SENSOR,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_SYSTEM_UK,
)

class UnexpectedError(Exception):
    """Other error."""

    pass


_LOGGER = logging.getLogger(__name__)


class Meteobridge:
    """Main class to retrieve the data from the Logger."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        Host: str,
        User: str,
        Pass: str,
        unit_system: str,
    ):
        self._host = Host
        self._user = User
        self._pass = Pass
        self._unit_system = unit_system.lower()
        self.sensor_data = {}

        self.req = session

    async def update(self) -> dict:
        """Updates the sensor data."""
        await self._get_sensor_data()
        return self.sensor_data

    async def BinarySensors(self) -> dict:
        """Returns the Binary Sensor Definitions."""
        return await self._get_binary_sensors()

    async def _get_binary_sensors(self) -> None:
        """ Returns a class with Binary Sensor Definitions."""
        items = []

        # Raining
        item = {
            "sensor_entity": "raining",
            "sensor_name": "Raining",
            "icon_on": "water",
            "icon_off": "water-off",
            "device_class": DEVICE_CLASS_NONE
        }
        items.append(HomeAssistantBinarySensors(item))
        # Low Battery
        item = {
            "sensor_entity": "lowbattery",
            "sensor_name": "Battery Status",
            "icon_on": "battery",
            "icon_off": "battery-10",
            "device_class": DEVICE_CLASS_NONE
        }
        items.append(HomeAssistantBinarySensors(item))
        # Freezing
        item = {
            "sensor_entity": "freezing",
            "sensor_name": "Freezing",
            "icon_on": "thermometer-plus",
            "icon_off": "thermometer-minus",
            "device_class": DEVICE_CLASS_NONE,
        }
        items.append(HomeAssistantBinarySensors(item))
   
        return items

    async def _get_sensor_data(self) -> None:
        """Gets the sensor data from the Meteobridge Logger"""

        dataTemplate = "[DD]/[MM]/[YYYY];[hh]:[mm]:[ss];[th0temp-act:0];[thb0seapress-act:0];[th0hum-act:0];[wind0avgwind-act:0];[wind0dir-avg5.0:0];[rain0total-daysum:0];[rain0rate-act:0];[th0dew-act:0];[wind0chill-act:0];[wind0wind-max1:0];[th0lowbat-act.0:0];[thb0temp-act:0];[thb0hum-act.0:0];[th0temp-dmax:0];[th0temp-dmin:0];[wind0wind-act:0];[th0heatindex-act.1:0];[uv0index-act:0];[sol0rad-act:0];[th0temp-mmin.1:0];[th0temp-mmax.1:0];[th0temp-ymin.1:0];[th0temp-ymax.1:0];[wind0wind-mmax.1:0];[wind0wind-ymax.1:0];[rain0total-mmax.1:0];[rain0total-ymax.1:0];[rain0rate-mmax.1:0];[rain0rate-ymax.1:0];[forecast-text:]"
        endpoint = f"http://{self._user}:{self._pass}@{self._host}/cgi-bin/template.cgi?template={dataTemplate}"

        async with self.req.get(endpoint,) as response:
            if response.status == 200:
                content = await response.read()
                decoded_content = content.decode("utf-8")

                cr = csv.reader(decoded_content.splitlines(), delimiter=";")
                rows = list(cr)
                cnv = Conversion()

                for values in rows:
                    self._timestamp = datetime.strptime(
                        values[0] + " " + values[1], "%d/%m/%Y %H:%M:%S"
                    )

                    self._outtemp = cnv.temperature(float(values[2]), self._unit_system)
                    self._press = cnv.pressure(float(values[3]), self._unit_system)
                    self._outhum = values[4]
                    self._windspeedavg = cnv.speed(float(values[5]), self._unit_system)
                    self._windbearing = int(float(values[6]))
                    self._winddir = cnv.wind_direction(float(values[6]))
                    self._raintoday = cnv.volume(float(values[7]), self._unit_system)
                    self._rainrate = cnv.rate(float(values[8]), self._unit_system)
                    self._outdew = cnv.temperature(float(values[9]), self._unit_system)
                    self._windchill = cnv.temperature(
                        float(values[10]), self._unit_system
                    )
                    self._windgust = cnv.speed(float(values[11]), self._unit_system)
                    self._lowbat = values[12]
                    self._intemp = cnv.temperature(float(values[13]), self._unit_system)
                    self._inhum = values[14]
                    self._temphigh = cnv.temperature(
                        float(values[15]), self._unit_system
                    )
                    self._templow = cnv.temperature(
                        float(values[16]), self._unit_system
                    )
                    self._windspeed = cnv.speed(float(values[17]), self._unit_system)
                    self._heatindex = cnv.temperature(
                        float(values[18]), self._unit_system
                    )
                    self._uvindex = float(values[19])
                    self._solarrad = float(values[20])
                    self._feels_like = cnv.feels_like(
                        self._outtemp,
                        self._heatindex,
                        self._windchill,
                        self._unit_system,
                    )
                    self._tempmmin = cnv.temperature(
                        float(values[21]), self._unit_system
                    )
                    self._tempmmax = cnv.temperature(
                        float(values[22]), self._unit_system
                    )
                    self._tempymin = cnv.temperature(
                        float(values[23]), self._unit_system
                    )
                    self._tempymax = cnv.temperature(
                        float(values[24]), self._unit_system
                    )
                    self._windmmax = cnv.speed(float(values[25]), self._unit_system)
                    self._windymax = cnv.speed(float(values[26]), self._unit_system)
                    self._rainmmax = cnv.volume(float(values[27]), self._unit_system)
                    self._rainymax = cnv.volume(float(values[28]), self._unit_system)
                    self._rainratemmax = cnv.volume(
                        float(values[29]), self._unit_system
                    )
                    self._rainrateymax = cnv.volume(
                        float(values[30]), self._unit_system
                    )
                    self._fc = values[31]

                    self._isfreezing = True if float(self._outtemp) < 0 else False
                    self._israining = True if float(self._rainrate) > 0 else False
                    self._islowbat = True if float(self._lowbat) > 0 else False

                item = {
                    "in_temperature": self._intemp,
                    "in_humidity": self._inhum,
                    "temperature": self._outtemp,
                    "temphigh": self._temphigh,
                    "templow": self._templow,
                    "humidity": self._outhum,
                    "dewpoint": self._outdew,
                    "windbearing": self._windbearing,
                    "winddirection": self._winddir,
                    "windspeedavg": self._windspeedavg,
                    "windspeed": self._windspeed,
                    "windgust": self._windgust,
                    "windchill": self._windchill,
                    "heatindex": self._heatindex,
                    "feels_like": self._feels_like,
                    "pressure": self._press,
                    "rainrate": self._rainrate,
                    "raintoday": self._raintoday,
                    "uvindex": self._uvindex,
                    "solarrad": self._solarrad,
                    "lowbattery": self._islowbat,
                    "raining": self._israining,
                    "freezing": self._isfreezing,
                    "forecast": self._fc,
                    "time": self._timestamp.strftime("%d-%m-%Y %H:%M:%S"),
                    "temp_mmin": self._tempmmin,
                    "temp_mmax": self._tempmmax,
                    "temp_ymin": self._tempymin,
                    "temp_ymax": self._tempymax,
                    "windspeed_mmax": self._windmmax,
                    "windspeed_ymax": self._windymax,
                    "rain_mmax": self._rainmmax,
                    "rain_ymax": self._rainymax,
                    "rainrate_mmax": self._rainratemmax,
                    "rainrate_ymax": self._rainrateymax,
                }
                self.sensor_data.update(item)
            else:
                raise UnexpectedError(
                    f"Fetching Meteobridge data failed: {response.status} - Reason: {response.reason}"
                )

    async def _get_sensor_data_new(self) -> None:
        """Gets the sensor data from the Meteobridge Logger"""

        dataTemplate = "[DD]/[MM]/[YYYY];[hh]:[mm]:[ss];[th0temp-act:0];[thb0seapress-act:0];[th0hum-act:0];[wind0avgwind-act:0];[wind0dir-avg5.0:0];[rain0total-daysum:0];[rain0rate-act:0];[th0dew-act:0];[wind0chill-act:0];[wind0wind-max1:0];[th0lowbat-act.0:0];[thb0temp-act:0];[thb0hum-act.0:0];[th0temp-dmax:0];[th0temp-dmin:0];[wind0wind-act:0];[th0heatindex-act.1:0];[uv0index-act:0];[sol0rad-act:0];[th0temp-mmin.1:0];[th0temp-mmax.1:0];[th0temp-ymin.1:0];[th0temp-ymax.1:0];[wind0wind-mmax.1:0];[wind0wind-ymax.1:0];[rain0total-mmax.1:0];[rain0total-ymax.1:0];[rain0rate-mmax.1:0];[rain0rate-ymax.1:0];[forecast-text:]"
        endpoint = f"http://{self._user}:{self._pass}@{self._host}/cgi-bin/template.cgi?template={dataTemplate}"

        async with self.req.get(endpoint,) as response:
            if response.status == 200:
                content = await response.read()
                decoded_content = content.decode("utf-8")

                cr = csv.reader(decoded_content.splitlines(), delimiter=";")
                rows = list(cr)
                cnv = Conversion()

                items = []
                for values in rows:
                    # Outside Temperature
                    item = {
                        "sensor_entity": "temperature",
                        "sensor_name": "Temperature",
                        "value": cnv.temperature(float(values[2]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Pressure
                    item = {
                        "sensor_entity": "pressure",
                        "sensor_name": "Pressure",
                        "value": cnv.pressure(float(values[3]), self._unit_system),
                        "unit": None,
                        "icon": "gauge",
                        "device_class": DEVICE_CLASS_PRESSURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Humidity
                    item = {
                        "sensor_entity": "humidity",
                        "sensor_name": "Humidity",
                        "value": values[4],
                        "unit": "%",
                        "icon": "gauge",
                        "device_class": DEVICE_CLASS_HUMIDITY,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Speed Average
                    item = {
                        "sensor_entity": "windspeedavg",
                        "sensor_name": "Wind Speed Avg",
                        "value": cnv.speed(float(values[5]), self._unit_system),
                        "unit": None,
                        "icon": "weather-windy",
                        "device_class": DEVICE_CLASS_WIND,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Bearing
                    item = {
                        "sensor_entity": "windbearing",
                        "sensor_name": "Wind Bearing",
                        "value": int(float(values[6])),
                        "unit": "°",
                        "icon": "compass-outline",
                        "device_class": DEVICE_CLASS_WIND_DIRECTION,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Direction Short Text
                    item = {
                        "sensor_entity": "winddirection",
                        "sensor_name": "Wind Direction",
                        "value": cnv.wind_direction(float(values[6])),
                        "unit": "",
                        "icon": "compass-outline",
                        "device_class": DEVICE_CLASS_WIND_DIRECTION,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Rain Today
                    item = {
                        "sensor_entity": "raintoday",
                        "sensor_name": "Rain today",
                        "value": cnv.volume(float(values[7]), self._unit_system),
                        "unit": None,
                        "icon": "weather-rainy",
                        "device_class": DEVICE_CLASS_RAIN,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Rain Rate
                    item = {
                        "sensor_entity": "rainrate",
                        "sensor_name": "Rain rate",
                        "value": cnv.rate(float(values[8]), self._unit_system),
                        "unit": None,
                        "icon": "weather-pouring",
                        "device_class": DEVICE_CLASS_RAINRATE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Outside Dewpoint
                    item = {
                        "sensor_entity": "dewpoint",
                        "sensor_name": "Dewpoint",
                        "value": cnv.temperature(float(values[9]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Outside Wind Chill
                    item = {
                        "sensor_entity": "windchill",
                        "sensor_name": "Wind Chill",
                        "value": cnv.temperature(float(values[10]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Gust
                    item = {
                        "sensor_entity": "windgust",
                        "sensor_name": "Wind Gust",
                        "value": cnv.speed(float(values[11]), self._unit_system),
                        "unit": None,
                        "icon": "weather-windy",
                        "device_class": DEVICE_CLASS_WIND,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Indoor Temperature
                    item = {
                        "sensor_entity": "in_temperature",
                        "sensor_name": "Indoor Temp",
                        "value": cnv.temperature(float(values[13]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Indoor Humidity
                    item = {
                        "sensor_entity": "in_humidity",
                        "sensor_name": "Indoor Hum",
                        "value": values[14],
                        "unit": "%",
                        "icon": "gauge",
                        "device_class": DEVICE_CLASS_HUMIDITY,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Temp High Today
                    item = {
                        "sensor_entity": "temphigh",
                        "sensor_name": "Temp High Today",
                        "value": cnv.temperature(float(values[15]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Temp Low Today
                    item = {
                        "sensor_entity": "templow",
                        "sensor_name": "Temp Low Today",
                        "value": cnv.temperature(float(values[16]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Speed
                    item = {
                        "sensor_entity": "windspeed",
                        "sensor_name": "Wind Speed",
                        "value": cnv.speed(float(values[17]), self._unit_system),
                        "unit": None,
                        "icon": "weather-windy",
                        "device_class": DEVICE_CLASS_WIND,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Heat Index
                    item = {
                        "sensor_entity": "heatindex",
                        "sensor_name": "Heat Index",
                        "value": cnv.temperature(float(values[18]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # UV Index
                    item = {
                        "sensor_entity": "uvindex",
                        "sensor_name": "UV Index",
                        "value": float(values[19]),
                        "unit": "UVI",
                        "icon": "weather-sunny-alert",
                        "device_class": DEVICE_CLASS_NONE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Solar Radiation
                    item = {
                        "sensor_entity": "solarrad",
                        "sensor_name": "Solar Radiation",
                        "value": float(values[20]),
                        "unit": "W/m2",
                        "icon": "weather-sunny",
                        "device_class": DEVICE_CLASS_NONE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Feels Like Temperature
                    self._feels_like = cnv.feels_like(
                        float(values[2]),
                        float(values[18]),
                        float(values[10]),
                        self._unit_system,
                    )
                    item = {
                        "sensor_entity": "feels_like",
                        "sensor_name": "Feels Like",
                        "value": self._feels_like,
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Temp Month Min
                    item = {
                        "sensor_entity": "temp_mmin",
                        "sensor_name": "Temp Month Min",
                        "value": cnv.temperature(float(values[21]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Temp Month Max
                    item = {
                        "sensor_entity": "temp_mmax",
                        "sensor_name": "Temp Month Max",
                        "value": cnv.temperature(float(values[22]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Temp Year Min
                    item = {
                        "sensor_entity": "temp_ymin",
                        "sensor_name": "Temp Year Min",
                        "value": cnv.temperature(float(values[23]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Temp Year Max
                    item = {
                        "sensor_entity": "temp_ymax",
                        "sensor_name": "Temp Year Max",
                        "value": cnv.temperature(float(values[24]), self._unit_system),
                        "unit": None,
                        "icon": "thermometer",
                        "device_class": DEVICE_CLASS_TEMPERATURE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Speed Month Max
                    item = {
                        "sensor_entity": "windspeed_mmax",
                        "sensor_name": "Wind Speed Month Max",
                        "value": cnv.speed(float(values[25]), self._unit_system),
                        "unit": None,
                        "icon": "weather-windy",
                        "device_class": DEVICE_CLASS_WIND,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Wind Speed Year Max
                    item = {
                        "sensor_entity": "windspeed_ymax",
                        "sensor_name": "Wind Speed Year Max",
                        "value": cnv.speed(float(values[26]), self._unit_system),
                        "unit": None,
                        "icon": "weather-windy",
                        "device_class": DEVICE_CLASS_WIND,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Rain Month Total
                    item = {
                        "sensor_entity": "rain_mmax",
                        "sensor_name": "Rain Month Total",
                        "value": cnv.volume(float(values[27]), self._unit_system),
                        "unit": None,
                        "icon": "weather-rainy",
                        "device_class": DEVICE_CLASS_RAIN,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Rain Year Total
                    item = {
                        "sensor_entity": "rain_ymax",
                        "sensor_name": "Rain Year Total",
                        "value": cnv.volume(float(values[28]), self._unit_system),
                        "unit": None,
                        "icon": "weather-rainy",
                        "device_class": DEVICE_CLASS_RAIN,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Rain Rate Month Max
                    item = {
                        "sensor_entity": "rainrate_mmax",
                        "sensor_name": "Rain rate Month Max",
                        "value": cnv.rate(float(values[29]), self._unit_system),
                        "unit": None,
                        "icon": "weather-pouring",
                        "device_class": DEVICE_CLASS_RAINRATE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Rain Rate Year Max
                    item = {
                        "sensor_entity": "rainrate_ymax",
                        "sensor_name": "Rain rate Year Max",
                        "value": cnv.rate(float(values[30]), self._unit_system),
                        "unit": None,
                        "icon": "weather-pouring",
                        "device_class": DEVICE_CLASS_RAINRATE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Forecast Text
                    item = {
                        "sensor_entity": "forecast",
                        "sensor_name": "Station Forecast",
                        "value": values[31],
                        "unit": "",
                        "icon": "text-short",
                        "device_class": DEVICE_CLASS_NONE,
                        "entity_type": ENTITY_TYPE_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))

                    self._isfreezing = True if float(float(values[2])) < 0 else False
                    self._israining = True if float(float(values[8])) > 0 else False
                    self._islowbat = True if float(values[12]) > 0 else False

                    # Raining
                    item = {
                        "sensor_entity": "raining",
                        "sensor_name": "Raining",
                        "value": self._israining,
                        "unit": "",
                        "icon": "water;water-off",
                        "device_class": DEVICE_CLASS_NONE,
                        "entity_type": ENTITY_TYPE_BINARY_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Low Battery
                    item = {
                        "sensor_entity": "lowbattery",
                        "sensor_name": "Battery Status",
                        "value": self._islowbat,
                        "unit": "",
                        "icon": "battery-10;battery",
                        "device_class": DEVICE_CLASS_NONE,
                        "entity_type": ENTITY_TYPE_BINARY_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))
                    # Freezing
                    item = {
                        "sensor_entity": "freezing",
                        "sensor_name": "Freezing",
                        "value": self._islowbat,
                        "unit": "",
                        "icon": "thermometer-minus;thermometer-plus",
                        "device_class": DEVICE_CLASS_NONE,
                        "entity_type": ENTITY_TYPE_BINARY_SENSOR,
                        "unit_system": self._unit_system
                    }
                    items.append(HomeAssistantData(item))

                # item = {
                #     "in_temperature": self._intemp,
                #     "in_humidity": self._inhum,
                #     "temperature": self._outtemp,
                #     "temphigh": self._temphigh,
                #     "templow": self._templow,
                #     "humidity": self._outhum,
                #     "dewpoint": self._outdew,
                #     "windbearing": self._windbearing,
                #     "winddirection": self._winddir,
                #     "windspeedavg": self._windspeedavg,
                #     "windspeed": self._windspeed,
                #     "windgust": self._windgust,
                #     "windchill": self._windchill,
                #     "heatindex": self._heatindex,
                #     "feels_like": self._feels_like,
                #     "pressure": self._press,
                #     "rainrate": self._rainrate,
                #     "raintoday": self._raintoday,
                #     "uvindex": self._uvindex,
                #     "solarrad": self._solarrad,
                #     "lowbattery": self._islowbat,
                #     "raining": self._israining,
                #     "freezing": self._isfreezing,
                #     "forecast": self._fc,
                #     "time": self._timestamp.strftime("%d-%m-%Y %H:%M:%S"),
                #     "temp_mmin": self._tempmmin,
                #     "temp_mmax": self._tempmmax,
                #     "temp_ymin": self._tempymin,
                #     "temp_ymax": self._tempymax,
                #     "windspeed_mmax": self._windmmax,
                #     "windspeed_ymax": self._windymax,
                #     "rain_mmax": self._rainmmax,
                #     "rain_ymax": self._rainymax,
                #     "rainrate_mmax": self._rainratemmax,
                #     "rainrate_ymax": self._rainrateymax,
                # }
                # self.sensor_data.update(item)
                return items
            else:
                raise UnexpectedError(
                    f"Fetching Meteobridge data failed: {response.status} - Reason: {response.reason}"
                )


class Conversion:

    """
    Conversion Class to convert between different units.
    WeatherFlow always delivers values in the following formats:
    Temperature: C
    Wind Speed: m/s
    Wind Direction: Degrees
    Pressure: mb
    Distance: km
    """

    def temperature(self, value, unit):
        if unit == UNIT_SYSTEM_IMPERIAL:
            # Return value F
            return round((value * 9 / 5) + 32, 1)
        else:
            # Return value C
            return round(value, 1)

    def volume(self, value, unit):
        if unit == UNIT_SYSTEM_IMPERIAL:
            # Return value in
            return round(value * 0.0393700787, 2)
        else:
            # Return value mm
            return round(value, 1)

    def rate(self, value, unit):
        if unit == UNIT_SYSTEM_IMPERIAL:
            # Return value in
            return round(value * 0.0393700787, 2)
        else:
            # Return value mm
            return round(value, 2)

    def pressure(self, value, unit):
        if unit == UNIT_SYSTEM_IMPERIAL:
            # Return value inHg
            return round(value * 0.0295299801647, 3)
        else:
            # Return value mb
            return round(value, 1)

    def speed(self, value, unit):
        if unit == UNIT_SYSTEM_IMPERIAL:
            # Return value in mi/h
            return round(value * 2.2369362921, 1)
        elif unit == "uk":
            # Return value in km/h
            return round(value * 3.6, 1)
        else:
            # Return value in m/s
            return round(value, 1)

    def distance(self, value, unit):
        if unit == UNIT_SYSTEM_IMPERIAL:
            # Return value in mi
            return round(value * 0.621371192, 1)
        else:
            # Return value in km
            return round(value, 0)

    def feels_like(self, temp, heatindex, windchill, unit):
        """ Return Feels Like Temp."""
        if unit == UNIT_SYSTEM_IMPERIAL:
            high_temp = 80
            low_temp = 50
        else:
            high_temp = 26.666666667
            low_temp = 10

        if float(temp) > high_temp:
            return float(heatindex)
        elif float(temp) < low_temp:
            return float(windchill)
        else:
            return temp

    def wind_direction(self, bearing):
        direction_array = [
            "N",
            "NNE",
            "NE",
            "ENE",
            "E",
            "ESE",
            "SE",
            "SSE",
            "S",
            "SSW",
            "SW",
            "WSW",
            "W",
            "WNW",
            "NW",
            "NNW",
            "N",
        ]
        direction = direction_array[int((bearing + 11.25) / 22.5)]
        return direction
