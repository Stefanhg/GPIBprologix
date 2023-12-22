import logging
import serial

logger = logging.getLogger(__name__)


class ResourceManager:
    """
    Controls the resources of the GpibPrologix
    """
    active_address = None
    """ Stores the active selected address """

    def __init__(self, comport, read_timeout_ms=1000, baud=115200, timeout=2):
        """
        Initializes the resource manager of the GpibPrologix
        :param comport: comport of the device. Example COM8, ttyS0
        :param read_timeout_ms: Read timeout of the GPIBPrologix in milliseconds
        :param baud: Baudrate of the GPIBPrologix.
        :param timeout: Timeout of Serial interface
        """
        logger.debug(f"Opening serial resource")
        self.inst = serial.Serial(comport, baudrate=baud, timeout=timeout)
        self.inst.write(f"++read_tmo_ms {read_timeout_ms}\n".encode())

    def open_resource(self, address):
        """
        Opens the resource and returns
        """
        return self.GpibPrologix(self.inst, address)

    def close(self):
        """
        Closes the opened object
        """
        self.inst.close()
        self.inst = None

    class GpibPrologix:

        def __init__(self, inst, address):
            self.address = address
            self.inst = inst

        def _select_address(self):
            """
            Selects which address objects uses if address is not already selected
            """
            if self.address != ResourceManager.active_address:
                logger.debug(f"selecting address {self.address}")
                self.inst.write(f"++addr {self.address}\n".encode())
                ResourceManager.active_address = self.address

        def write(self, data):
            """
            Write data to GPIB.
            Method ensures the correct address is selected when writing to target.
            :param data: Data to send
            :return:
            """
            logger.debug(f"Sending {data}")
            # section 7 of GPIB prologix's manual describes having to additional characters for
            # characters with escape code


            data = (data.replace('\x0A', '\x1b\x0A').replace('\x1D', '\x1b\x0D')
                    .replace('\x1b', '\x1b\x1b').replace('\x2b', '\x1b\x2b+'))
            data = f"{data}\n".encode()
            self._select_address()
            self.inst.write(data)

        def read(self) -> str:
            """
            Reads the next line of data available and returns it.
            """

            self.inst.write(b"++read eoi\n")
            data = self.inst.readline().decode('utf-8').rstrip()
            logger.debug(f"Read {data}")
            return data

        def query(self, data: str) -> str:
            """
            Send data and wait for data to return.
            :param data: Data to send
            :return:
            """
            self.write(data)
            return self.read()
