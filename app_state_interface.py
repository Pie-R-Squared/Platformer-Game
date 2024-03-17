from abc import ABC, abstractmethod

import pygame


class IAppState(ABC):

    @abstractmethod
    def start(self):
        """
        Setup everything we need to run the state.
        """

    @abstractmethod
    def stop(self):
        """
        Cleanup everything we don't need once the state is no longer running.
        """

    @abstractmethod
    def time_to_transition(self) -> bool:
        """
        Check if it is time to leave this state and transition to another.

        :return: True if it is time to stop the state, False if it is not.
        """

    @abstractmethod
    def get_transition_target(self) -> str:
        """
        Get the ID string of the new state to transition to
        """

    @abstractmethod
    def update(self, time_delta: float):
        """
        Update the state once per loop including the amount of time that has passed since the
        previous loop of the App.
        """

    @abstractmethod
    def process_event(self, event: pygame.event.Event):
        """
        Give the state a chance to respond to any pygame events that have been fired.

        :param event: A pygame event.
        """

    @abstractmethod
    def draw(self):
        """
        Draw this state to the application's window surface.
        """
