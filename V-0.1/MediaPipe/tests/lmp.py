import tinytuya

from types import SimpleNamespace

import math
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
lamp = tinytuya.BulbDevice(
    'eb6cf639a85ba6907by7ss',
    '192.168.0.109',
    'CGBlNgA==+v~1Lqc'
)


lamp.set_version(3.5)

status = lamp.status()
ligada = status.get('dps', {}).get('20', False)

lamp.turn_on()

print("Asasdas")