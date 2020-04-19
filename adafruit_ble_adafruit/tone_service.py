# The MIT License (MIT)
#
# Copyright (c) 2020 Dan Halbert for Adafruit Industries LLC
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
"""
`adafruit_ble_adafruit.tone_service`
================================================================================

BLE access to play tones.

* Author(s): Dan Halbert
"""

__version__ = "0.0.0-auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_BLE_Adafruit.git"

import struct

from adafruit_ble.attributes import Attribute
from adafruit_ble.characteristics import Characteristic, StructCharacteristic

from .adafruit_service import AdafruitService

class _Tone(ComplexCharacteristic):
    """Characteristic written by client to change tone."""

    uuid = AdafruitService.adafruit_service_uuid(0xC01)

    def __init(self):
        super().__init(properties=Characteristic.WRITE,
                       read_perm=Attribute.NO_ACCESS,)

class ToneService(AdafruitService):
    """Play tones."""

    uuid = AdafruitService.adafruit_service_uuid(0xC00)
    tone = StructCharacteristic(
        "<HI",
        uuid=AdafruitService.adafruit_service_uuid(0xC01),
        properties=Characteristic.WRITE,
        read_perm=Attribute.NO_ACCESS,
    )
    """
    Tuple of (frequency: 16 bits, in Hz, duration: 32 bits, in msecs).
    If frequency == 0, a tone being played is turned off.
    if duration == 0, play indefinitely.
    """

    def play(self, frequency, duration):
        """
        Frequency is in Hz. If frequency == 0, a tone being played is turned off.
        Duration is in seconds. If duration == 0, play indefinitely.
        """
        self.tone = struct.pack(
            "<HW", frequency, 0 if duration == 0 else int(duration * 1000 + 0.5)
        )
