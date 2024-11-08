"""! @Brief A buffer for CAN messages."""
#
# @file can_buffer.py
#
# @brief A buffer for CAN messages.
#
# @section description_can_buffer Description
# This module represents the CanBuffer class.
#
# @section libraries_can_buffer Libraries/Modules
# - Queue class from vtime module
# - TimeEvent class from vtime module
# - CanMessage class from framework/hardware_interfaces/drivers/common/definitions/interfaces module
#
# @section notes_can_buffer Notes
# - None.
#
# @section todo_can_buffer TODO
# - None.
#
# @section author_can_buffer Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 29/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved

from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    CanMessage,
)
from framework.support.vtime import Queue, TimeEvent


class CanBuffer(Queue[CanMessage]):
    """
    A buffer for CAN messages. It can be configured to filter messages based on.
    """

    def __init__(self, mbx_id: int, maxsize: int = 0) -> None:
        super().__init__(maxsize)
        self.mbx_id = mbx_id
        self._mask: int | None = None
        self._msg_id: int | None = None
        self.read_request = TimeEvent()

    def set_mask(self, mask: int) -> None:
        """
        ! Set mask for buffer.
        """
        self._mask = mask

    def set_filter(self, msg_id: int) -> None:
        """
        ! Set filter for buffer.
        """
        self._msg_id = msg_id

    def check_filter(self, item: CanMessage) -> bool:
        """
        ! Check filter for buffer.
        """
        if self._msg_id and item.arbitration_id != self._msg_id:
            return False
        return True

    def put_can_msg(
        self, item: CanMessage, block: bool = True, timeout: float | None = None
    ) -> bool:
        """
        ! Put CAN message in buffer.
        """
        if self.check_filter(item):
            super().put(item, block, timeout)
            return True
        return False
