import glob
import os

import struct


class Struct:

    def __init__(self, **entries):
        self.__dict__.update(entries)


def convert_to_str(s):
    '''Function to convert data into float'''
    return str(struct.unpack("<f", struct.pack("<I", s))[0])


def count_num_files(path):
    list_of_files = glob.glob(path + str("/*.csv"))
    return len(list_of_files) + 1


def write_csv_header(csv_file, header):
    with open(csv_file, 'w') as f:
        f.write(header)


def find_param_numbers(params_provided, params_to_record):
    provided_array = params_provided.split(",")
    record_array = params_to_record.split(",")
    param_numbers = [provided_array.index(x) for x in record_array]
    return param_numbers


def find_tty_usb(idVendor, idProduct):
    """find_tty_usb('067b', '2302') -> '/dev/ttyUSB0'"""
    # Note: if searching for a lot of pairs, it would be much faster to search
    # for the enitre lot at once instead of going over all the usb devices
    # each time.
    for dnbase in os.listdir('/sys/bus/usb/devices'):
        dn = join('/sys/bus/usb/devices', dnbase)
        if not os.path.exists(join(dn, 'idVendor')):
            continue
        idv = open(join(dn, 'idVendor')).read().strip()
        if idv != idVendor:
            continue
        idp = open(join(dn, 'idProduct')).read().strip()
        if idp != idProduct:
            continue
        for subdir in os.listdir(dn):
            if subdir.startswith(dnbase + ':'):
                for subsubdir in os.listdir(join(dn, subdir)):
                    if subsubdir.startswith('ttyUSB'):
                        return join('/dev', subsubdir)
