"""! @brief Fluidics Connection Tests."""
##
# @file test_fluidics.py
#
# @brief Fluidics Connection Tests.
#
# @section description_test_fluidics Description
# This module representing the TestConnection testing class.
#
# @section libraries_test_fluidics Libraries/Modules
# - reports module (local)
# - fluidics module (local)
#   - Access to Fluidics class.
#
# @section notes_test_fluidics Notes
# - None.
#
# @section todo_test_fluidics TODO
# - None.
#
# @section author_test_fluidics Author(s)
# - Created by:
#   - Maksym Masalov <maksym.masalov@globallogic.com> on 06/09/2024.
# - Modified by:
#   - Ihor Pryyma ihor.pryyma@globallogic.com on 17/09/2024.
#
# Copyright (c) 2024 Alcon & GlobalLogic.  All rights reserved.

from framework.apps.fluidics import Fluidics
from framework.support.reports import report


class TestConnection:
    """! Connection Tests."""

    def test_connection(self, fluidics: Fluidics) -> None:
        """! This test tries to connect with Fluidics."""
        with report.TestStep("Connect with Fluidics."):
            fluidics.vtime.sleep(0.5)

    def test_buttons(self, fluidics: Fluidics) -> None:
        """
        ! This test tries to play with button (latch_eject) on Fluidics.
        """
        with report.TestStep("Test buttons in Fluidics"):
            hold_time = 0.2
            for button_name, hw_button in fluidics.buttons.get_all_buttons():
                fluidics.vtime.sleep(0.3)
                hw_button.press_button(hold_time)

                fluidics.vtime.sleep(0.3)
                hw_button.release_button()

                fluidics.vtime.sleep(0.3)
                hw_button.press_button(hold_time)

                fluidics.vtime.sleep(0.3)
                hw_button.release_button()
            pass

        with report.TestStep("Finish with Buttons"):
            fluidics.vtime.sleep(0.3)
            pass
