from __future__ import annotations
from abc import ABC, abstractmethod

# The common state interface for all the states
class State():
    @property
    def program(self):
        return self._program

    @program.setter
    def program(self, program):
        self._program = program

    @property
    def processor(self):
        return self._processor
    
    @processor.setter
    def processor(self, processor):
        self._processor = processor

    @property
    def GUIhelper(self):
        return self._GUIhelper
    
    @GUIhelper.setter
    def GUIhelper(self, GUIhelper):
        self._GUIhelper = GUIhelper
 
    @abstractmethod
    def go_to_open_menu(self):
        pass
    
    @abstractmethod
    def go_to_menu(self):
        pass

    @abstractmethod
    def go_to_add_server(self):
        pass

    @abstractmethod
    def go_to_remove_server(self):
        pass

    @abstractmethod
    def go_to_update_servers(self):
        pass

    @abstractmethod
    def go_to_server_state(self, server_name):
        pass

    @abstractmethod
    def go_to_sanity_check(self, server_name):
        pass

    @abstractmethod
    def go_to_connect_server(self, server_name):
        pass

    @abstractmethod
    def go_to_update_certificate(self, server_name):
        pass

    @abstractmethod
    def go_to_upgrade_server(self, server_name):
        pass

    @abstractmethod
    def go_to_server_menu(self, server_name):
        pass

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def show_all_servers(self):
        pass

    @abstractmethod
    def show_server_list(self, cs_list):
        pass

    @abstractmethod
    def show_server(self, cs_server):
        pass
    
    @abstractmethod
    def show_options(self):
        pass

    @abstractmethod
    def show_banner(self):
        pass
