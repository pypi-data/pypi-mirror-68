from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple, Optional


class BaseEventHandler(ABC):
    def __init__(self, event_message: Dict[str, Any]):
        self.event_message = event_message

    @abstractmethod
    def my_source(self) -> str:
        pass

    @abstractmethod
    def generate_response(self) -> Tuple[Optional[str], Optional[str]]:
        pass

    @property
    def event_source(self) -> str:
        return self.event_message['source']
