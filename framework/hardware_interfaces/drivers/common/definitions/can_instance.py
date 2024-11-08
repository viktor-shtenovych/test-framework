"""! @Brief CAN instance definition."""

#
# @file can_instance.py
#
# @brief CAN instance definition.
#
# @section description_can_instance Description
# This module represents the CANInstance class.
#
# @section libraries_can_instance Libraries/Modules
# - dataclasses standard library
# - typing standard library
# - Dict class from typing module
# - Any class from typing module
# - CanBuffer class from framework/hardware_interfaces/drivers/common/definitions/can_buffer module
# - CanMessage class from framework/hardware_interfaces/drivers/common/definitions/interfaces module
# - MCMode class from framework/hardware_interfaces/protoc/mpc5777c/mpc5777c_mcan_driver_pb2 module
#
# @section notes_can_instance Notes
# - None.
#
# @section todo_can_instance TODO
# - None.
#
# @section author_mpc5777c_mcan_driver Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 29/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved
import dataclasses
from typing import Dict, Any, Union

from framework.hardware_interfaces.drivers.common.definitions.can_buffer import (
    CanBuffer,
)
from framework.hardware_interfaces.drivers.common.definitions.interfaces import (
    CanMessage,
)
from framework.hardware_interfaces.protoc.mpc5777c.mpc5777c_mcan_driver_pb2 import (
    MCMode,
)

from framework.support.vtime import Queue


@dataclasses.dataclass
class CANInstance:
    """
    ! CAN instance.
    """

    in_msgs: Queue[CanMessage]
    out_buffers: Dict[int, CanBuffer]
    freeze_mode: Union[MCMode, bool]
    irq_id: int
    read_request_pending: Dict[int, Any]
