"""! @Brief Enumeration of MCU types."""

#
# @file mcu_types.py
#
# @brief Enumeration of MCU types.
#
# @section description_mcu_types Description
# This module represents the enumeration of MCU types.
#
# @section libraries_mcu_types Libraries/Modules
# - enum standard library
#
# @section notes_mcu_types Notes
# - None.
#
# @section todo_mcu_types TODO
# - None.
#
# @section author_mcu_types Author(s)
# - Created by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 09/10/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic. All rights reserved.
from enum import StrEnum


class MCUType(StrEnum):
    """
    ! Enumeration of MCU types.
    """

    S32K148 = "s32k148"
    MPC5777C = "mpc5777c"
