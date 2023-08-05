#!/usr/bin/env python
from pyzerproc import discover_devices


def test_discover_devices(adapter):
    """Test the CLI."""
    def scan(*args, **kwargs):
        """Simulate a scanning response"""
        return [
            {
                'address': 'AA:BB:CC:11:22:33',
                'name': 'LEDBlue-CC112233',
            },
            {
                'address': 'AA:BB:CC:44:55:66',
                'name': 'LEDBlue-CC445566',
            },
            {
                'address': 'DD:EE:FF:11:22:33',
                'name': 'Other',
            },
            {
                'address': 'DD:EE:FF:44:55:66',
                'name': None,
            },
        ]

    adapter.scan.side_effect = scan

    assert discover_devices(15) == [
        'AA:BB:CC:11:22:33',
        'AA:BB:CC:44:55:66',
    ]

    adapter.start.assert_called_with(reset_on_start=False)
    adapter.scan.assert_called_with(timeout=15)
    adapter.stop.assert_called_once()
