from utils import find_tty_usb, convert_to_str
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
from datetime import datetime


class SmartMeter(object):

    """
    1. Sets up a smart meter connection
    2. Specifies a serial port to connect to
    3. Methods to read and write data (to csv)
    """

    def __init__(self, retries=2, com_method='rtu', baudrate=19200, stopbits=1, parity='N', bytesize=8, timeout=0.1):
        """Sets up parameters for modbus connection to the smart meter

        Parameters
        ----------
        retries :  int, default=2
             The number of times a packet read request must be made
        com_method : string, default='rtu'
            Mode of connection
        baudrate : int, default=19200
            Baudrate set on the smart meter, eg. 9600, 19200
        stopbits : int, default=1
            Number of stopbits set on the smart meter, eg. 1
        parity : string, default='N'
            Parity set on the smart meter, eg. 'N':None, 'E':Even
        bytesize : int, default=8
            Size of packet, eg. 8
        timeout : float, default=0.1
            Number of seconds before a request times out, eg. 0.1
        """
        self.retries = retries
        self.com_method = com_method
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout

    def connect(self, vendor="", product="", meter_port=None):
        """Connects to a specific port (if specified). Else, if the device details
        of USB-Modbus device are given, finds the port on which they are attached.
        This may be needed as the serial port on RPi was observed to.

        Parameters
        ----------
        vendor: string
        product: string

        Returns
        --------
        client : ModbusSerialClient
        """
        if meter_port is None:
            self.meter_port = find_tty_usb(vendor, product)
        else:
            self.meter_port = meter_port
        #print("Connecting to %s" % (self.meter_port))
        self.client = ModbusClient(
            retries=self.retries, method=self.com_method,
            baudrate=self.baudrate, stopbits=self.stopbits, parity=self.parity,
            bytesize=self.bytesize, timeout=self.timeout, port=self.meter_port)
        #print("Connected to smart meter over: %s" % (self.client.port))
        return self.client

    def read_from_meter(self, meter_id, base_register, block_size,
                        params_indices):
        """Reads data from meter correpsonding to the param indices
        specified

        Parameters
        -----------

        meter_id : ID set on the meter (eg. 1, 2), int
        base_register : Base register for block of registers to read, int
        block_size : Number of register bytes in this block, int
        params_indices : List of indices relative to base_register, list

        Returns
        -------
        data: Comma separated values correpsonding to parameters whose indices
        were specified
        """
        try:
            binary_data = self.client.read_holding_registers(
                base_register, block_size, unit=meter_id)
        except:
            # Sleep for some time and again try to connect
            time.sleep(0.5)
            self.connect(vendor="", product="", meter_port=self.meter_port)
            binary_data = self.client.read_holding_registers(
                base_register, block_size, unit=meter_id)

        data = ""
        for i in range(0, (block_size - 1), 2):
            for j in params_indices:
                if(j == i):
                    data = data + str(datetime.now()) + "," + \
                        convert_to_str(
                            (binary_data.registers[i + 1] << 16) + binary_data.registers[i])

        data = data[:-1] + "\n"
        return data

    def write_csv(self, csv_path, data):
        """Writes a comma separted row of data into the csv

        Parameters
        ----------
        csv_path : Complete path of the CSV file
        data : string representation of row to write
        """
        with open(csv_path, 'a') as f:
            f.write(data)
