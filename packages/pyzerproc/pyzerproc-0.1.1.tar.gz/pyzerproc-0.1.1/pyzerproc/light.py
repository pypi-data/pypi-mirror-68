"""Device class"""
from binascii import hexlify
import logging
import queue

_LOGGER = logging.getLogger(__name__)

CHARACTERISTIC_COMMAND_WRITE = "0000ffe9-0000-1000-8000-00805f9b34fb"
CHARACTERISTIC_NOTIFY_VALUE = "0000ffe4-0000-1000-8000-00805f9b34fb"

NOTIFICATION_RESPONSE_TIMEOUT = 5


class Light():
    """Represents one connected light"""

    def __init__(self, address):
        self.address = address
        self.adapter = None
        self.device = None
        self.notification_queue = queue.Queue(maxsize=1)

    def connect(self, auto_reconnect=False):
        """Connect to this light"""
        import pygatt

        _LOGGER.info("Connecting to %s", self.address)

        self.adapter = pygatt.GATTToolBackend()
        self.adapter.start(reset_on_start=False)
        self.device = self.adapter.connect(
            self.address, auto_reconnect=auto_reconnect)

        _LOGGER.debug("Connected to %s", self.address)

        self.device.subscribe(CHARACTERISTIC_NOTIFY_VALUE,
                              callback=self._handle_data)

    def disconnect(self):
        """Connect to this light"""
        if self.adapter:
            self.adapter.stop()
            self.adapter = None
            self.device = None

    def turn_on(self):
        """Turn on the light"""
        _LOGGER.info("Turning on %s", self.address)
        self._write(CHARACTERISTIC_COMMAND_WRITE, b'\xCC\x23\x33')
        _LOGGER.debug("Turned on %s", self.address)

    def turn_off(self):
        """Turn off the light"""
        _LOGGER.info("Turning off %s", self.address)
        self._write(CHARACTERISTIC_COMMAND_WRITE, b'\xCC\x24\x33')
        _LOGGER.debug("Turned off %s", self.address)

    def set_color(self, r, g, b):
        """Set the color of the light

        Accepts red, green, and blue values from 0-255
        """
        for value in (r, g, b):
            if not 0 <= value <= 255:
                raise ValueError(
                    "Value {} is outside the valid range of 0-255")

        _LOGGER.info("Changing color of %s to #%02x%02x%02x",
                     self.address, r, g, b)

        # Normalize to 0-31, the supported range of these lights
        r = int(r * 31 / 255)
        g = int(g * 31 / 255)
        b = int(b * 31 / 255)
        color_string = "{:c}{:c}{:c}".format(r, g, b).encode()

        value = b'\x56' + color_string + b'\x00\xF0\xAA'
        self._write(CHARACTERISTIC_COMMAND_WRITE, value)
        _LOGGER.debug("Changed color of %s", self.address)

    def _handle_data(self, handle, value):
        """Handle an incoming notification message."""
        _LOGGER.debug("Got handle '%s' and value %s", handle, hexlify(value))
        try:
            self.notification_queue.put_nowait(value)
        except queue.Full:
            _LOGGER.debug("Discarding duplicate response", exc_info=True)

    def get_state(self):
        """Get the current state of the light"""
        # Clear the queue if a value is somehow left over
        try:
            self.notification_queue.get_nowait()
        except queue.Empty:
            pass

        self._write(CHARACTERISTIC_COMMAND_WRITE, b'\xEF\x01\x77')

        try:
            response = self.notification_queue.get(
                timeout=NOTIFICATION_RESPONSE_TIMEOUT)
        except queue.Empty as ex:
            raise TimeoutError("Timeout waiting for response") from ex

        on_off_value = int(response[2])

        r = int(response[6])
        g = int(response[7])
        b = int(response[8])

        if on_off_value == 0x23:
            is_on = True
        elif on_off_value == 0x24:
            is_on = False
        else:
            is_on = None

        # Normalize and clamp from 0-31, to 0-255
        r = int(min(r * 255 / 31, 255))
        g = int(min(g * 255 / 31, 255))
        b = int(min(b * 255 / 31, 255))

        state = LightState(is_on, (r, g, b))

        _LOGGER.info("Got state of %s: %s", self.address, state)

        return state

    def _write(self, uuid, value):
        """Internal method to write to the device"""
        if not self.device:
            raise RuntimeError(
                "Light {} is not connected".format(self.address))

        _LOGGER.debug("Writing 0x%s to characteristic %s", value.hex(), uuid)
        self.device.char_write(uuid, value)
        _LOGGER.debug("Wrote 0x%s to characteristic %s", value.hex(), uuid)


class LightState():
    """Represents the current state of the light"""
    __slots__ = 'is_on', 'color',

    def __init__(self, is_on, color):
        """Create the state object"""
        self.is_on = is_on
        self.color = color

    def __repr__(self):
        """Return a string representation of the state object"""
        return "<LightState is_on='{}' color='{}'>".format(
            self.is_on, self.color)
