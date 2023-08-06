"""Defines the Data Classes used."""

from pymeteobridgeio.const import (
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_PRESSURE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_RAIN,
    DEVICE_CLASS_RAINRATE,
    DEVICE_CLASS_WIND,
    DEVICE_CLASS_NONE,
    ENTITY_TYPE_BINARY_SENSOR,
    UNIT_SYSTEM_IMPERIAL,
    UNIT_SYSTEM_METRIC,
    UNIT_SYSTEM_UK,
)

class HomeAssistantBinarySensors:
    """A representation of Binary Sensors created in Home Assistant."""

    def __init__(self, data):
        self._sensor_entity = data["sensor_entity"]
        self._sensor_name = data["sensor_name"]
        self._icon_on = data["icon_on"]
        self._icon_off = data["icon_off"]
        self._device_class = data["device_class"]

    @property
    def sensor_entity(self) -> str:
        """Sensor Entity Name."""
        return self._sensor_entity

    @property
    def sensor_name(self) -> str:
        """Sensor Friendly Name."""
        return self._sensor_name

    @property
    def icon_on(self) -> str:
        """Sensor Icon On State."""
        return f"mdi:{self._icon_on}"

    @property
    def icon_off(self) -> str:
        """Sensor Icon Off State."""
        return f"mdi:{self._icon_off}"

    @property
    def device_class(self) -> str:
        """Sensors Device Class."""
        return self._device_class


class HomeAssistantSensors:
    """A representation of Sensors created in Home Assistant."""

    def __init__(self, data):
        self._sensor_entity = data["sensor_entity"]
        self._sensor_name = data["sensor_name"]
        self._icon = data["icon"]
        self._device_class = data["device_class"]
        self._unit = data["unit"]

    @property
    def sensor_entity(self) -> str:
        """Sensor Entity Name."""
        return self._sensor_entity

    @property
    def sensor_name(self) -> str:
        """Sensor Friendly Name."""
        return self._sensor_name

    @property
    def icon(self) -> str:
        """Sensor Icon."""
        return f"mdi:{self._icon}"

    @property
    def device_class(self) -> str:
        """Sensors Device Class."""
        return self._device_class

    @property
    def unit(self) -> str:
        """Sensor Unit."""
        if self._unit_system == UNIT_SYSTEM_IMPERIAL:
            if self._device_class == DEVICE_CLASS_TEMPERATURE:
                return "°F"
            elif self._device_class == DEVICE_CLASS_PRESSURE:
                return "inHg"
            elif self._device_class == DEVICE_CLASS_WIND:
                return "mph"
            elif self._device_class == DEVICE_CLASS_RAIN:
                return "in"
            elif self._device_class == DEVICE_CLASS_RAINRATE:
                return "in/h"
            else:
                return self._unit
        elif self._unit_system == UNIT_SYSTEM_UK:
            if self._device_class == DEVICE_CLASS_TEMPERATURE:
                return "°C"
            elif self._device_class == DEVICE_CLASS_PRESSURE:
                return "hPa"
            elif self._device_class == DEVICE_CLASS_WIND:
                return "km/h"
            elif self._device_class == DEVICE_CLASS_RAIN:
                return "mm"
            elif self._device_class == DEVICE_CLASS_RAINRATE:
                return "mm/h"
            else:
                return self._unit
        else:
            if self._device_class == DEVICE_CLASS_TEMPERATURE:
                return "°C"
            elif self._device_class == DEVICE_CLASS_PRESSURE:
                return "hPa"
            elif self._device_class == DEVICE_CLASS_WIND:
                return "m/s"
            elif self._device_class == DEVICE_CLASS_RAIN:
                return "mm"
            elif self._device_class == DEVICE_CLASS_RAINRATE:
                return "mm/h"
            else:
                return self._unit

class HomeAssistantData:
    """A representation of Data used by Home Assistant Sensors."""

    def __init__(self, data):
        self._sensor_entity = data["sensor_entity"]
        self._sensor_name = data["sensor_name"]
        self._value = data["value"]
        self._unit = data["unit"]
        self._icon = data["icon"]
        self._device_class = data["device_class"]
        self._entity_type = data["entity_type"]
        self._unit_system = data["unit_system"]

    @property
    def sensor_entity(self) -> str:
        """Sensor Entity Name."""
        return self._sensor_entity

    @property
    def sensor_name(self) -> str:
        """Sensor Friendly Name."""
        return self._sensor_name

    @property
    def entity_type(self) -> str:
        """Return Entity Type."""
        return self._entity_type

    @property
    def value(self):
        """Sensor Value"""
        return self._value

    @property
    def unit(self) -> str:
        """Sensor Unit."""
        if self._unit_system == UNIT_SYSTEM_IMPERIAL:
            if self._device_class == DEVICE_CLASS_TEMPERATURE:
                return "°F"
            elif self._device_class == DEVICE_CLASS_PRESSURE:
                return "inHg"
            elif self._device_class == DEVICE_CLASS_WIND:
                return "mph"
            elif self._device_class == DEVICE_CLASS_RAIN:
                return "in"
            elif self._device_class == DEVICE_CLASS_RAINRATE:
                return "in/h"
            else:
                return self._unit
        elif self._unit_system == UNIT_SYSTEM_UK:
            if self._device_class == DEVICE_CLASS_TEMPERATURE:
                return "°C"
            elif self._device_class == DEVICE_CLASS_PRESSURE:
                return "hPa"
            elif self._device_class == DEVICE_CLASS_WIND:
                return "km/h"
            elif self._device_class == DEVICE_CLASS_RAIN:
                return "mm"
            elif self._device_class == DEVICE_CLASS_RAINRATE:
                return "mm/h"
            else:
                return self._unit
        else:
            if self._device_class == DEVICE_CLASS_TEMPERATURE:
                return "°C"
            elif self._device_class == DEVICE_CLASS_PRESSURE:
                return "hPa"
            elif self._device_class == DEVICE_CLASS_WIND:
                return "m/s"
            elif self._device_class == DEVICE_CLASS_RAIN:
                return "mm"
            elif self._device_class == DEVICE_CLASS_RAINRATE:
                return "mm/h"
            else:
                return self._unit

    @property
    def icon(self) -> str:
        """Sensor Icon."""
        if self._entity_type == ENTITY_TYPE_BINARY_SENSOR:
            return self._icon
        else:
            return f"mdi:{self._icon}"

    @property
    def device_class(self) -> str:
        """Sensors Device Class."""
        return self._device_class

        