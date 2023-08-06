import os
import subprocess
from time import sleep
from functools import wraps


class OneWire:

    setup_delay: int = 3
    one_wire_dir: str = "/sys/devices/w1_bus_master1"
    paths: dict = {
        "slave_count": f"{one_wire_dir}/w1_master_slave_count",
        "slaves": f"{one_wire_dir}/w1_master_slaves"
    }

    def __init__(self, gpio: int):
        self.gpio = str(gpio)
        self.ready = self.__init_one_wire()

    def __insert_kernel_module(self) -> None:
        """ enables w1 kernel module for a given GPIO pin"""
        arg_bus = f"bus0=0,{self.gpio},0"
        subprocess.call(["insmod", "w1-gpio-custom", arg_bus])

    def __check_one_wire_dir(self) -> bool:
        """ sysfs check if kernel w1 module is loaded """
        return os.path.isdir(self.one_wire_dir)

    def __init_one_wire(self) -> bool:
        """ initialize w1 bus """
        for i in range(3):
            if self.__check_one_wire_dir():
                return True
            self.__insert_kernel_module()
            sleep(self.setup_delay)

    def __is_ready(original_func):
        """ in-class decorator, that checks if w1 is initialized properly """
        @wraps(original_func)
        def wrapped(instance, *args, **kwargs):
            if instance.ready:
                return original_func(instance, *args, **kwargs)
            else:
                raise Exception("OneWire was not initialized properly.")
        return wrapped

    @__is_ready
    def has_slaves(self) -> bool:
        """ checks for registered devices """
        with open(self.paths['slave_count']) as fd:
            slave_count = [i.rstrip() for i in fd.readlines()]
        return False if len(slave_count) == 0 else True

    def is_registered(self, address: str) -> bool:
        """ check if address exists in the list of registered devices """
        slave_list = self.get_addresses()
        return True if address in slave_list else False

    @__is_ready
    def get_addresses(self) -> str:
        """ returns list of registered slaves """
        with open(self.paths['slaves']) as fd:
            slave_list = fd.read().split('\n')
        del slave_list[-1]  # always empty string
        return slave_list

    def get_one_address(self) -> str:
        """ return 1st available address """
        return self.get_addresses()[0]

    @__is_ready
    def read_device(self, address: str = None) -> str:
        """ Read from w1 slave on address """
        if not address:
            address = self.get_one_address()
        with open(os.path.join(self.one_wire_dir, address, "w1_slave")) as fd:
            data = fd.readlines()
        return data
