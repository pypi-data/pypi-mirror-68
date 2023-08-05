# Anyleaf

## For use with the Anyleaf pH sensor

## Example use:
```python
import time

import board
import busio
from anyleaf import PhSensor, CalPt, CalSlot


def main():
    i2c = busio.I2C(board.SCL, board.SDA)
    ph_sensor = PhSensor(i2c)

    # 2 or 3 pt calibration both give acceptable results.
    # Calibrate with known values
    ph_sensor.calibrate_all(
        CalPt(0., 7., 25.), CalPt(-0.18, 4., 25.), CalPt(0.18, 4., 25.)
    )

    # Or:
    #ph_sensor.calibrate(CalSlot.One, CalPt(0.18, 4., 25.))
    #ph_sensor.calibrate(CalSlot.Two, CalPt(0., 7., 23.))

    # Ideally, store the calibration parameters somewhere, so they persist
    # between program runs.

    while True:
        pH = ph_sensor.read()
        print(f"pH: {pH}")
        time.sleep(.5)


if __name__ == "__main__":
    main()


```