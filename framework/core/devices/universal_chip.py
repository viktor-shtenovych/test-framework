"""! @Brief Universal chip simulation."""

##
# The UniversalChip class is a class that represents a universal chip simulation.
# @file universal_chip.py
#
# @section description_universal_chip Description
# This module represents the UniversalChip class.
#
# @section libraries_universal_chip Libraries/Modules
# - UniversalChip module (local)
#   - Access to UniversalChip class.
#
# @section notes_universal_chip Notes
# - None.
#
# @section todo_universal_chip TODO
# - None.
#
# @section author_universal_chip Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 24/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from typing import Dict

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    DataStream,
)
from framework.support.reports import logger


class UniversalChip(DataStream):
    """
    Universal chip simulation.

    This is supposed to be used for chips where static response data can be defined
    for specific requests.
    """

    def __init__(
        self,
        response_data_map: Dict[bytes, bytes],
        default_response: bytes | None = None,
    ) -> None:
        self.response_data_map: Dict[bytes, bytes] = response_data_map
        self.request_data: bytes | None = None
        self.default_response = default_response

    def read(self) -> bytes:
        """
        Read the data.

        Returns:
            bytes: The data.
        """
        if self.request_data is None and self.default_response is None:
            raise RuntimeError("No write received before read")

        logger.debug(f"UniversalChip: Request data for {self.request_data!r}")
        if self.request_data in self.response_data_map:
            logger.debug(
                f"UniversalChip: Sending data: {self.response_data_map[self.request_data]!r}"
            )
            return self.response_data_map[self.request_data]
        elif self.default_response is not None:
            return self.default_response

        raise KeyError(f"No response defined for request data {self.request_data!r}.")

    def write(self, request_data: bytes) -> None:
        """
        Write the data.

        Args:
            request_data (bytes): The data.
        """
        self.request_data = request_data
