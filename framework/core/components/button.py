from abc import abstractmethod, ABC
from typing import List, Tuple

from framework.core.peripherals.digital_pin import DigitalInput
from framework.support.vtime import vtime_manager


class Button(DigitalInput):
    """
    ! Switches/buttons access: see300055529-SCH_P7.pdf.

    see:
      - application/fsw_ctl/app/src/fsw_io_mec_context.cpp
      - application/fsw_ctl/nal_3/inc/nal/fsw_ctl_alias.h
      - nal/s32k148_common/inc/nal/s32k148_pins.h
    """

    def press_button(self, hold_time: float = 0) -> None:
        """
        ! Presses the button for a specified time.
        """
        self.state = True
        if hold_time:
            vtime_manager.sleep(hold_time)

    def release_button(self) -> None:
        """
        ! Releases the button.
        """
        self.state = False


class Buttons(ABC):
    """
    ! Represents the buttons of the app.
    """

    @abstractmethod
    def get_all_buttons(self) -> List[Tuple[str, Button]]:
        """
        ! Get all buttons.

        @return A list of tuples with the button name and the button object.
        """
