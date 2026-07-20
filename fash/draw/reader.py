from fash.core.exceptions import CursorPositionError
from typing import Tuple
from io import UnsupportedOperation
import sys
import termios
import tty
import re

class Reader:
    def __init__(self):
        '''Get file descriptor from terminal where this python code is running'''
        try:
            self.file_descriptor: int = sys.stdin.fileno()
        except UnsupportedOperation:
            '''
            TODO: Refactor and define a terminal reading strategy
                - This exception only happens in pytest. Reader should extend a BaseReader class and pytest 
                must create a FakeReader passed to drawer through Dependency Injection
                - We need to determine if a Reader class really should be in the draw module
                - Currently there is no definition on how user input will be defined and handled in widgets
                so this class is a 'temporary' measure wich only solves the drawer need for the current cursor position
            '''
            pass

    def save_terminal_settings(self):
        self.terminal_settings = termios.tcgetattr(self.file_descriptor)
    
    def restore_last_terminal_settings(self):
         termios.tcsetattr(self.file_descriptor, termios.TCSADRAIN, self.terminal_settings)

    def enter_raw_mode(self):
        tty.setraw(self.file_descriptor)

    def get_cursor_pos(self) -> Tuple[int,int]:
        self.save_terminal_settings()
        self.enter_raw_mode()
        
        print("\033[6n", end="")
        sys.stdout.flush()
        
        response = ""
        
        while True:
            ch = sys.stdin.read(1)
            response += ch
            if ch == "R":
                break
        
        self.restore_last_terminal_settings()
        
        match = re.search(r"\[(\d+);(\d+)R", response)
        
        if not match:
            raise CursorPositionError("Reader: Could not read cursor position")

        row, col = int(match.group(1)), int(match.group(2))

        return row, col