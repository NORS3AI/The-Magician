"""State machine for managing game state transitions."""

from enum import Enum, auto
from typing import Optional, Dict, Callable, Any


class GameState(Enum):
    """All possible game states."""
    MAIN_MENU = auto()
    LOGIN = auto()
    REGISTER = auto()
    CHARACTER_SELECT = auto()
    PLAYING = auto()
    COMBAT = auto()
    DIALOGUE = auto()
    INVENTORY = auto()
    STATS = auto()
    PAUSE = auto()
    QUIT = auto()


class StateMachine:
    """Manages game state transitions with validation."""

    def __init__(self, initial_state: GameState = GameState.MAIN_MENU):
        """
        Initialize state machine.

        Args:
            initial_state: Starting game state
        """
        self.current_state = initial_state
        self.previous_state: Optional[GameState] = None
        self.state_data: Dict[str, Any] = {}
        self._transition_callbacks: Dict[GameState, Callable] = {}

    def transition_to(self, new_state: GameState, **data) -> bool:
        """
        Transition to a new state.

        Args:
            new_state: State to transition to
            **data: Optional data to pass to the new state

        Returns:
            True if transition was successful
        """
        if not self._can_transition(self.current_state, new_state):
            return False

        self.previous_state = self.current_state
        self.current_state = new_state
        self.state_data = data

        # Call transition callback if registered
        if new_state in self._transition_callbacks:
            self._transition_callbacks[new_state]()

        return True

    def _can_transition(self, from_state: GameState, to_state: GameState) -> bool:
        """
        Check if transition between states is valid.

        Args:
            from_state: Current state
            to_state: Desired state

        Returns:
            True if transition is allowed
        """
        # Define valid transitions
        valid_transitions = {
            GameState.MAIN_MENU: {
                GameState.LOGIN,
                GameState.REGISTER,
                GameState.CHARACTER_SELECT,
                GameState.QUIT
            },
            GameState.LOGIN: {
                GameState.MAIN_MENU,
                GameState.CHARACTER_SELECT
            },
            GameState.REGISTER: {
                GameState.MAIN_MENU,
                GameState.CHARACTER_SELECT,
                GameState.LOGIN
            },
            GameState.CHARACTER_SELECT: {
                GameState.MAIN_MENU,
                GameState.PLAYING
            },
            GameState.PLAYING: {
                GameState.COMBAT,
                GameState.DIALOGUE,
                GameState.INVENTORY,
                GameState.STATS,
                GameState.PAUSE,
                GameState.MAIN_MENU,
                GameState.QUIT
            },
            GameState.COMBAT: {
                GameState.PLAYING,
                GameState.INVENTORY,
                GameState.QUIT
            },
            GameState.DIALOGUE: {
                GameState.PLAYING,
                GameState.QUIT
            },
            GameState.INVENTORY: {
                GameState.PLAYING,
                GameState.COMBAT,
                GameState.QUIT
            },
            GameState.STATS: {
                GameState.PLAYING,
                GameState.QUIT
            },
            GameState.PAUSE: {
                GameState.PLAYING,
                GameState.MAIN_MENU,
                GameState.QUIT
            },
            GameState.QUIT: set()  # No transitions from QUIT
        }

        # Allow self-transitions (staying in same state)
        if from_state == to_state:
            return True

        return to_state in valid_transitions.get(from_state, set())

    def register_callback(self, state: GameState, callback: Callable) -> None:
        """
        Register a callback for when entering a state.

        Args:
            state: State to register callback for
            callback: Function to call when entering state
        """
        self._transition_callbacks[state] = callback

    def get_data(self, key: str, default: Any = None) -> Any:
        """
        Get state data.

        Args:
            key: Data key
            default: Default value if key not found

        Returns:
            Value associated with key
        """
        return self.state_data.get(key, default)

    def set_data(self, key: str, value: Any) -> None:
        """
        Set state data.

        Args:
            key: Data key
            value: Value to store
        """
        self.state_data[key] = value

    def go_back(self) -> bool:
        """
        Return to previous state if possible.

        Returns:
            True if successful
        """
        if self.previous_state is None:
            return False

        return self.transition_to(self.previous_state)

    def is_in_gameplay(self) -> bool:
        """
        Check if currently in gameplay states.

        Returns:
            True if in PLAYING, COMBAT, DIALOGUE, INVENTORY, or STATS
        """
        return self.current_state in {
            GameState.PLAYING,
            GameState.COMBAT,
            GameState.DIALOGUE,
            GameState.INVENTORY,
            GameState.STATS
        }

    def reset(self) -> None:
        """Reset state machine to initial state."""
        self.current_state = GameState.MAIN_MENU
        self.previous_state = None
        self.state_data.clear()
