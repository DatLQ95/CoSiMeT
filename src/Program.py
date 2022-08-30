from StateMachine.StateMachine import State
from ProgramStates import *
from GUIHelper import GUIHelper
from CSProcessor import CSProcessor

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
