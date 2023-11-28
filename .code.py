import time
import board
import busio
import adafruit_sdcard
import storage
import adafruit_dht
from adafruit_datetime import datetime

# Initialize I2C bus
i2c = busio.I2C(board.SCL, board.SDA)

# Initialize SD card
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
cs = board.D10  # Change this to the actual chip select pin for your SD card module
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Open CSV file on SD card
file_path = "/sd/sensor_data.csv"
with open(file_path, "a") as file:
    file.write("Timestamp,Temperature_C,Humidity_Percentage\n")

# Initialize DHT20 sensor on D4 pin, change to the actual pin you are using
dht = adafruit_dht.DHT20(board.D4)

while True:
    try:
        # Read data from the DHT20 sensor
        temperature_celsius = dht.temperature
        humidity_percentage = dht.relative_humidity

        # Get current UTC timestamp as a datetime object
        utc_now = datetime.utcnow()

        # Format data as a CSV line
        csv_line = "{},{},{}\n".format(utc_now.isoformat(), temperature_celsius, humidity_percentage)

        # Open file in append mode and write the CSV line
        with open(file_path, "a") as file:
            file.write(csv_line)

        # Wait for 5 minutes before the next reading
        time.sleep(300)

    except Exception as e:
        print("Error:", e)
        # Handle exceptions (e.g., if sensor reading fails) to prevent the program from crashing
        time.sleep(1)

