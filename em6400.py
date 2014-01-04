from __future__ import print_function

import os

from smart_meter import SmartMeter
from utils import count_num_files, write_csv_header, find_param_numbers
from utils import Struct
from configuration import DATA_PATH


# Change these two lines in accordance with your meter configuration
from configuration import _6400
meter_config = Struct(**_6400)

meter_config.param_indices = find_param_numbers(
    meter_config.params_provided, meter_config.params_to_record)


# Find the CSV file to write in
csv_file_number = count_num_files(DATA_PATH)
csv_file_path = os.path.join(DATA_PATH, str(csv_file_number) + ".csv")

# Write header into the CSV
write_csv_header(csv_file_path, "Timestamp," +
                 meter_config.params_provided + "\n")

# Instantiate smartmeter
smart_meter = SmartMeter(meter_config.retries, meter_config.com_method,
                         meter_config.baudrate, meter_config.stopbits,
                         meter_config.parity, meter_config.bytesize,
                         meter_config.timeout)

# Make a connection
smart_meter.connect(meter_config.vendor, meter_config.product)

# Read and write infinitely
while True:
    data = smart_meter.read_from_meter(
        meter_config.meter_id, meter_config.base_register,
        meter_config.block_size, meter_config.param_indices)
    smart_meter.write_csv(csv_file_path, data)
