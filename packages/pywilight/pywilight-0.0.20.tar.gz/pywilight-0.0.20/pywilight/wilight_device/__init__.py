"""Base WiLight Device class."""

import collections
import logging
import sched
import socket
import time
import threading

import asyncio
from collections import deque
import logging
import codecs
import binascii

from ..const import (
    CONF_ITEMS,
    CONNECTION_TIMEOUT,
    DATA_DEVICE_REGISTER,
    DEFAULT_KEEP_ALIVE_INTERVAL,
    DEFAULT_PORT,
    DEFAULT_RECONNECT_INTERVAL,
    DOMAIN,
    WL_TYPES,
)
from ..support import (
    check_config_ex_len,
    get_item_sub_types,
    get_item_type,
    get_num_items,
)
#from ..protocol import WiLightClient  # noqa F401


LOG = logging.getLogger(__name__)


class UnknownService(Exception):
    """Exception raised when a non-existent service is called."""

    pass


class Device(object):
    """Base object for WiLight devices."""

    def __init__(self, host, serial_number, type, mode, key, rediscovery_enabled=True):
        """Create a WiLight device."""
        self._host = host
        self._port = 46000
        self._serial_number = serial_number
        self._type = type
        self._mode = mode
        self._key = key
        self.rediscovery_enabled = rediscovery_enabled
        self._retrying = False
        self._device_id = f"WL{serial_number}"
        self._name = f"WiLight Device - {serial_number}"
        self._items = self._config_items()
        self._client = None
        self._update_lock = None
        self.status_callbacks = {}
        # self._client = self._config_cliente()

    def _config_cliente(self):
        """Create WiLight Client Fake class."""
        client = WiLightClientFake(device_id=None, host=None, port=None, model=None, config_ex=None,
                            disconnect_callback=None,
                            reconnect_callback=None,
                            loop=None, logger=None,
                            timeout=1000, reconnect_interval=1000,
                            keep_alive_interval=1000)

        return client

    def _config_items(self):
        """
        Config items .

        I configure the items according to the input data.
        """
        #self._items = []
        items = []

        if self._type not in WL_TYPES:
            _LOGGER.warning("WiLight %s with unsupported type %s", device_id, self._type)
            return

        if not check_config_ex_len(self._type, self._mode):
            _LOGGER.warning("WiLight %s with error in mode %s", device_id, self._mode)
            return

        def get_item_name(s_i):
            """Get item name."""
            return f"{self._device_id}_{s_i}"

        num_items = get_num_items(self._type, self._mode)

        for i in range(0, num_items):

            index = f"{i:01x}"
            item_name = get_item_name(f"{i+1:01x}")
            item_type = get_item_type(i+1, self._type, self._mode)
            item_sub_type = get_item_sub_types(i+1, self._type, self._mode)
            item = {}
            item["index"] = index
            item["name"] = item_name
            item["type"] = item_type
            item["sub_type"] = item_sub_type
            items.append(item)

        return items

    def _reconnect_with_device_by_discovery(self):
        """
        Scan network to find the device again.

        WiLight tend to change their ip address when roter restarts.
        Whenever requests throws an error, we will try to find the device again
        on the network and update this device.
        """

        # Put here to avoid circular dependency
        from ..discovery import discover_devices

        # Avoid retrying from multiple threads
        if self._retrying:
            return

        self._retrying = True
        LOG.info("Trying to reconnect with %s", self._name)
        # We will try to find it 5 times, each time we wait a bigger interval
        try_no = 0

        while True:
            found = discover_devices(ssdp_st=None, max_devices=1,
                                     match_serial=self.serialnumber)

            if found:
                LOG.info("Found %s again, updating local values", self._name)

                # pylint: disable=attribute-defined-outside-init
                self.__dict__ = found[0].__dict__
                self._retrying = False
                #self._config_items()

                return

            wait_time = try_no * 5

            LOG.info(
                "%s Not found in try %i. Trying again in %i seconds",
                self._name, try_no, wait_time)

            if try_no == 5:
                LOG.error(
                    "Unable to reconnect with %s in 5 tries. Stopping.",
                    self._name)
                self._retrying = False

                return

            time.sleep(wait_time)

            try_no += 1

    def reconnect_with_device(self):
        """Re-probe & scan network to rediscover a disconnected device."""
        if self.rediscovery_enabled:
            if (self.serialnumber):
                self._reconnect_with_device_by_discovery()
        else:
            LOG.warning("Rediscovery was requested for device %s, "
                        "but rediscovery is disabled. Ignoring request.",
                        self._name)

    def register_status_callback(self, callback, index):
        """Register a callback which will fire when state changes."""
        self.logger.warning('register_status_callback %s : %s, %s', self.device_id, index, callback)
        #if self.status_callbacks.get(index, None) is None:
        #    self.status_callbacks[index] = []
        #self.status_callbacks[index].append(callback)
        self.status_callbacks[index].callback

    def set_update_lock(self, update_lock=None):
        """Set client connection for WiLight device."""
        self._update_lock = update_lock

    def set_client(self, client=None):
        """Set client connection for WiLight device."""
        self._client = client

    @property
    def host(self):
        """Return the host of the device."""
        return self._host

    @property
    def port(self):
        """Return the port of the device."""
        return self._port

    @property
    def serial_number(self):
        """Return the serial number of the device."""
        return self._serial_number

    @property
    def type(self):
        """Return the type of the device."""
        return self._type

    @property
    def mode(self):
        """Return the mode of the device."""
        return self._mode

    @property
    def key(self):
        """Return the key of the device."""
        return self._key

    @property
    def update_lock(self):
        """Return the update_lock of the device."""
        return self._update_lock

    @property
    def client(self):
        """Return the client of the device."""
        return self._client

    @property
    def items(self):
        """Return the items of the device."""
        #self._config_items()
        return self._items

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def device_id(self):
        """Return the device_id of the device."""
        return self._device_id
