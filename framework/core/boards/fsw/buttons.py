from typing import Tuple, List

from framework.core.boards.fsw.hw_board import HwBoard
from framework.core.components.button import Button, Buttons


class FswButtons(Buttons):
    """
    ! A class that implements the Buttons driver for FootSwitch.
    """

    def __init__(self, board: HwBoard) -> None:
        self.right_vertical = board.right_vertical
        self.right_horizontal = board.right_horizontal
        self.left_vertical = board.left_vertical
        self.left_horizontal = board.left_horizontal
        self.left_heel = board.left_heel
        self.right_heel = board.right_heel

    def get_all_buttons(self) -> List[Tuple[str, Button]]:
        """
        ! Get all FootSwitch buttons.

        @return A list of tuples with the button name and the button object.
        """
        return [
            ("right_vertical", self.right_vertical),
            ("right_horizontal", self.right_horizontal),
            ("left_vertical", self.left_vertical),
            ("left_horizontal", self.left_horizontal),
            ("left_heel", self.left_heel),
            ("right_heel", self.right_heel),
        ]
