# Anyleaf

## For use with the Anyleaf pH sensor

## Example use:
```python
import time

import board
import busio
from anyleaf import PhSensor, CalPt


def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    ph_sensor = PhSensor(i2c)

    # Can use 2 or 3-pt calibration.
    ph_sensor.calibrate(
        CalPt(0., 7., 25.), CalPt(-0.18, 4., 25.), CalPt(0.18, 4., 25.)
    )

    while True:
        pH = ph_sensor.read()
        print(f"pH: {pH}")
        time.sleep(.5)


if __name__ == "__main__":
    main()


```