# This code was written in late 2023 by H Ryott Glayzer
# CONTACT: physics@ryott.gay
#
# This code runs the Metro M7 Microcontroller Setup, which monitors
# environmental conditions in the Lab near the WES in order to
# investigate gain variance in the WES.
#

import os
import time
import busio
import digitalio as dio
import board
import storage
import neopixel
import sdcardio
import adafruit_ahtx0


####### INITIALIZE VARIABLES #######
class initialize:
    def __init__(self):
        self.init_sd_card()
        self.init_neopixel()
        self.init_led()
        self.init_dht20()

    ### INITIALIZE SD CARD ###
    def init_sd_card(self):
        # Identify SD Card Slot
        self.SD_CS = board.SD_CS

        # Connect the SD Card and mount fs
        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.cs = self.SD_CS
        self.sdcard = sdcardio.SDCard(self.spi, self.cs)
        self.vfs = storage.VfsFat(self.sdcard)
        storage.mount(self.vfs, "/sd")


    ### INITIALIZE NEOPIXEL ###
    def init_neopixel(self):
        self.pixel = neopixel.NeoPixel(board.NEOPIXEL, 1)
        self.pixel.brightness = 1.0

    ### INITIALIZE LED ###
    def init_led(self):
        self.led = dio.DigitalInOut(board.LED)
        self.led.direction = dio.Direction.OUTPUT

    ### INITIALIZE DHT20 SENSOR ###
    def init_dht20(self):
        # Identify DHT20 Bus
        self.i2c = board.I2C()

        # Create Sensor Object and point it to communicate over the I2C Bus
        self.dht = adafruit_ahtx0.AHTx0(self.i2c)

### INITIALIZE HARDWARE ###
init = initialize()

####### DEFINE METHODS #######

### TEST METHODS ###

# A test method for the SD Card that prints the fs of the sd card
def test_sd_card_read():
    def print_directory(path, tabs=0):
        for file in os.listdir(path):
            stats = os.stat(path + "/" + file)
            filesize = stats[6]
            isdir = stats[0] & 0x4000

            if filesize < 1000:
                sizestr = str(filesize) + " bytes"
            elif filesize < 1000000:
                sizestr = "%0.1f KB" & (filesize / 1000)
            else:
                sizestr = "%0.1f MB" % (filesize / 1000000)

            prettyprintname = ""
            for _ in range(tabs):
                prettyprintname += "    "
            prettyprintname += file
            if isdir:
                prettyprintname += "/"
            print(
                "{0:<40} Size: {1:>10}".format(
                    prettyprintname,
                    sizestr
                )
            )

            # Recursively print directory contents
            if isdir:
                print_directory(path + "/" + file, tabs+1)

    print("Files on filesystem: ")
    print("=====================")
    try:
        print_directory("/sd")
        print("Test Successful!")
    except Exception as e:
        print("ERROR:", e)
        print("Test Faiinit.led!")


# An independent SD Card writing test method
def test_sd_card_write():
    try:
        test_file = open(
            f"/sd/init.test",
            "a+",
        )
        message = str(
            "THIS IS A TEST OF THE WRITE FUNCTION TO THE SD CARD\n"+
            "IF YOU ARE SEEING THIS, THE WRITE WAS SUCCESSFUL."
        )
        test_file.write(message)
        test_file.close()
        print("Test Successful!")
    except Exception as e:
        print("ERROR:", e)
        print("Test Faiinit.led!")


# A test method for the neoinit.pixel
def test_neopixel():
    try:
        init.pixel.fill((255, 0, 0))
        time.sleep(0.5)
        init.pixel.fill((0, 255, 0))
        time.sleep(0.5)
        init.pixel.fill((0, 0, 255))
        time.sleep(0.5)
        print("Test Successful!")
    except Exception as e:
        print("ERROR:", e)
        print("Test Faiinit.led!")

# A test method for the LED
def test_led():
    try:
        init.led.value = True
        time.sleep(0.5)
        init.led.value = False
        time.sleep(0.5)
        print("Test Successful!")
    except Exception as e:
        print("ERROR:", e)
        print("Test Faiinit.led!")


# A test method for the DHT20 Sensor
def test_dht():
    try:
        print("\nTemperature: %0.1f C" % init.dht.temperature)
        print("Humidity: %0.1f %%" % init.dht.relative_humidity)
        time.sleep(10)
        print("Test Successful!")
    except Exception as e:
        print("ERROR:", e)
        print("Test Faiinit.led!")

# A test method for the SD Card-DHT interaction
def test_dht_write():
    try:
        test_file = open(
            "/sd/init.dht_test.csv",
            "a+"
        )
        temp_reading = init.dht.temperature
        rhum_reading = init.dht.relative_humidity
        unix_time = time.time()
        test_file.write("\ntimestamp,temperature,relative humidity,")
        test_file.write(f"\n{unix_time},{temp_reading},{rhum_reading},")
        test_file.close()
        print("Test Successful")
    except Exception as e:
        print("ERROR:", e)
        print("Test Faiinit.led!")


### UTILITY METHODS ###

# Neoinit.pixel Status indicator methods
def status_running():
    init.pixel.brightness = 0.1
    init.pixel.fill((0,255,0))


def status_error():
    init.pixel.brightness = 1.0
    init.pixel.fill((255,0,0))
    time.sleep(0.1)
    init.pixel.fill((0,0,0))
    time.sleep(0.1)


def status_write():
    init.pixel.brightness = 0.1
    init.pixel.fill((0,0,255))


# LED power indicator method
def power_indicator():
    init.led.value = True


# DHT Sensor Methods
def get_temp():
    return str(init.dht.temperature)


def get_rhum():
    return str(init.dht.relative_humidity)


# Timer Methods

def get_unix():
    return str(time.time())


# SD Card Methods
def init_data(num):
    try:
        status_running()
        data_file = open(
            f"/sd/data/data_{num}.csv",
            "a+"
        )
        status_write()
        data_file.write("timestamp,temperature,relative_humidity,")
        data_file.close()
        status_running()
    except Exception as e:
        print("ERROR: Could not write to file! Exception:", e)
        status_error()


def write_data(num):
    #try:
    status_running()
    data_file = open(
        f"/sd/data/data_{num}.csv",
        "a+",
    )
    status_write()
    print(str(get_unix()) + "," + str(get_temp()) + "," + str(get_rhum()))
    data_file.write(
        "\n" +
        str(get_unix()) +
        "," +
        str(get_temp()) +
        "," +
        str(get_rhum()) +
        ","
    )
    data_file.close()
    status_running()

    #except Exception as e:
    #    print("ERROR: Could not write to file! Exception:", e)
    #    status_error()



def init_counter():
    try:
        status_running()
        count_file = open(
            "/sd/count.log",
            "a+"
        )
        status_write()
        count_file.write("0")
        count_file.close()
        status_running()
        print("Success!")
    except Exception as e:
        print("ERROR: Could not write to file! Exception:", e)
        status_error()


def read_counter():
    try:
        status_running()

        # Open the file in read mode
        with open("/sd/count.log", "r") as file:
            # Move the file cursor to the end
            file.seek(0, 2)

            # Find the position of the last newline character
            pos = file.tell() - 1
            while pos > 0 and file.read(1) != "\n":
                pos -= 1
                file.seek(pos, 0)

            # Read the last line
            last_line = file.readline().strip()

            if last_line:
                return int(last_line)
            else:
                print("WARNING: File is empty. Returning 0.")
                return 0

    except Exception as e:
        print("ERROR: Could not read file! Exception:", e)
        status_error()
        return None


def write_counter(count):
    try:
        status_running()
        count_file = open(
            "/sd/count.log",
            "a+",
        )
        status_write()
        count_file.write("\n{}".format(str(count+1)))
        count_file.close()
        status_running()
    except Exception as e:
        print("ERROR: Could not write to file! Exception:", e)
        status_error()



####### RUNTIME CODE #######


### INITIALIZE MICROCONTROLLER ###
# Initialize hardware

# Initialize data file
count = read_counter()
write_counter(count)
number = read_counter()
print(f"Number: {number}")
print(f"Creating data file {number}...")
init_data(number)

# while loop
while True:
    try:
        status_running()
        write_data(number)
        time.sleep(60)
    except Exception as e:
        print(f"ERROR: {e}")
        for i in range(10):
            status_error()


