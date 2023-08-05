"""Device discovery code"""
import logging

_LOGGER = logging.getLogger(__name__)


def discover_devices(timeout=10):
    """Returns addresses of nearby lights"""
    _LOGGER.info("Starting scan for local devices")

    import pygatt
    adapter = pygatt.GATTToolBackend()
    adapter.start(reset_on_start=False)

    addresses = []
    try:
        for device in adapter.scan(timeout=timeout):
            # Improvements welcome
            if device['name'] and device['name'].startswith('LEDBlue-'):
                _LOGGER.info(
                    "Discovered %s: %s", device['address'], device['name'])
                addresses.append(device['address'])
    finally:
        adapter.stop()

    _LOGGER.info("Scan complete")
    return addresses
