from src.StateMachine.StateMachine import State
from src.ProgramStates import *
from src.GUIHelper import GUIHelper
from src.CSProcessor import CSProcessor

class Program:

    def __init__(self):
        self._state = None
        self.GUIhelper = GUIHelper()
        self.processor = CSProcessor()
        self.setProgramState(LoginState())

    def setProgramState(self, state: State):
        self._state = state
        self._state.program = self

    def run(self):
        self._state.execute()
