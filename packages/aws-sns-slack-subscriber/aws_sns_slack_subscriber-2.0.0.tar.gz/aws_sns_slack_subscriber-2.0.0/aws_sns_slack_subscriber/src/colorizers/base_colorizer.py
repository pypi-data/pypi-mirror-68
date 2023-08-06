from abc import ABC, abstractmethod
from typing import List, Optional


class BaseColorizer(ABC):
    def __init__(self, message: str):
        self.message = message

    @abstractmethod
    def matches(self) -> List[str]:
        pass

    @abstractmethod
    def slack_color(self) -> str:
        pass

    def match(self) -> Optional[str]:
        for match in self.matches():
            if match == '*':
                return self.slack_color()

            if match in self.message:
                return self.slack_color()
