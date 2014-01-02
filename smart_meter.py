from utils import find_tty_usb, convert_to_str
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time


class SmartMeter(object):

    def __init__(self, retries, com_method, baudrate,
                 stopbits, parity, bytesize, timeout):
        self.retries = retries
        self.com_method = com_method
        self.baudrate = baudrate
        self.stopbits = stopbits
        self.parity = parity
        self.bytesize = bytesize
        self.timeout = timeout

    def connect(self, vendor, product):
        self.meter_port = find_tty_usb(vendor, product)
        print("Connecting to %s" % (self.meter_port))
        self.client = ModbusClient(
            retries=self.retries, method=self.com_method,
            baudrate=self.baudrate, stopbits=self.stopbits, parity=self.parity,
            bytesize=self.bytesize, timeout=self.timeout)
        print("Connected")
        print self.client.port

    def read_from_meter(self, meter_id, base_register, block_size,
                        params_indices):
        binary_data = self.client.read_holding_registers(
            base_register, block_size, unit=meter_id)
        data = ""
        for i in range(0, (block_size - 1), 2):
            for j in params_indices:
                if(j == i):
                    data = data + str(int(time.time())) + "," + convert_to_str(binary_data.registers[i + 1] << 16 +
                                                                               binary_data.registers[i])
        data = data[:-1] + "\n"
        return data

    def write_csv(csv_path, data):
        with open(csv_path, 'a') as f:
            f.write(data)
