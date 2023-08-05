"""Base WiLight Device class."""

import logging
#import time

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


LOG = logging.getLogger(__name__)


class UnknownService(Exception):
    """Exception raised when a non-existent service is called."""

    pass


class Device(object):
    """Base object for WiLight devices."""

    def __init__(self, host, serial_number, type, mode, key,
                                      rediscovery_enabled=True):
        """Create a WiLight device."""
        self.host = host
        self.port = 46000
        self.retrying = False
        self.serial_number = serial_number
        self.type = type
        self.mode = mode
        self.key = key
        self.device_id = f"WL{serial_number}"
        self.name = f"WiLight Device - {serial_number}"
        self.rediscovery_enabled = rediscovery_enabled
        self.items = []
        self.client = None

    def _config_items(self):
        """
        Config items .

        I configure the items according to the input data.
        """
        self.items = []

        if self.type not in WL_TYPES:
            _LOGGER.warning("WiLight %s with unsupported type %s", device_id, self.type)
            return

        if not check_config_ex_len(self.type, self.mode):
            _LOGGER.warning("WiLight %s with error in mode %s", device_id, self.mode = mode)
            return

        def get_item_name(s_i):
            """Get item name."""
            return f"{self.device_id}_{s_i}"

        num_items = get_num_items(self.type, self.mode)

        for i in range(0, num_items):

            index = f"{i:01x}"
            item_name = get_item_name(f"{i+1:01x}")
            item_type = get_item_type(i, self.type, self.mode)
            item_sub_type = get_item_sub_types(i, self.type, self.mode)
            item = {}
            item["index"] = index
            item["item_name"] = item_name
            item["type"] = item_type
            item["sub_type"] = item_sub_type
            self.items.append(item)

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
        if self.retrying:
            return

        self.retrying = True
        LOG.info("Trying to reconnect with %s", self.name)
        # We will try to find it 5 times, each time we wait a bigger interval
        try_no = 0

        while True:
            found = discover_devices(ssdp_st=None, max_devices=1,
                                     match_serial=self.serialnumber)

            if found:
                LOG.info("Found %s again, updating local values", self.name)

                # pylint: disable=attribute-defined-outside-init
                self.__dict__ = found[0].__dict__
                self.retrying = False
                self._config_items()

                return

            wait_time = try_no * 5

            LOG.info(
                "%s Not found in try %i. Trying again in %i seconds",
                self.name, try_no, wait_time)

            if try_no == 5:
                LOG.error(
                    "Unable to reconnect with %s in 5 tries. Stopping.",
                    self.name)
                self.retrying = False

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
                        self.name)

    def set_client(self, client=None):
        """Set client connection for WiLight device."""

    @property
    def host(self):
        """Return the host of the device."""
        return self.host

    @property
    def port(self):
        """Return the port of the device."""
        return self.port

    @property
    def serialnumber(self):
        """Return the serial number of the device."""
        return self.serialnumber

    @property
    def type(self):
        """Return the type of the device."""
        return self.type

    @property
    def mode(self):
        """Return the mode of the device."""
        return self.mode

    @property
    def key(self):
        """Return the key of the device."""
        return self.key

    @property
    def client(self):
        """Return the key of the device."""
        return self.client

    @property
    def items(self):
        """Return the items of the device."""
        return self.items

    @property
    def name(self):
        """Return the name of the device."""
        return self.name
