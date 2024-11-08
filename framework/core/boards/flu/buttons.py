from typing import Tuple, List

from framework.core.boards.flu.hw_board import HwBoard
from framework.core.components.button import Button, Buttons


class FluButtons(Buttons):
    """
    ! A class that implements the Buttons driver for Fluidics.
    """

    def __init__(self, board: HwBoard) -> None:
        self.latch_eject = board.latch_eject

    def get_all_buttons(self) -> List[Tuple[str, Button]]:
        """
        ! Get all Fluidics buttons.

        @return A list of tuples with the button name and the button object.
        """
        return [
            ("latch_eject", self.latch_eject),
        ]
