from typing import List

try:
    from aws_sns_slack_subscriber.src.colorizers.base_colorizer import BaseColorizer
except ImportError:
    # noinspection PyUnresolvedReferences
    from colorizers.base_colorizer import BaseColorizer


class ErrorColorizer(BaseColorizer):
    def __init__(self, message: str):
        super().__init__(message)

    def matches(self) -> List[str]:
        return [
            "but with errors",
            "to RED",
            "During an aborted deployment",
            "Failed to deploy application",
            "Failed to deploy configuration",
            "has a dependent object",
            "is not authorized to perform",
            "Pending to Degraded",
            "Stack deletion failed",
            "Unsuccessful command execution",
            "You do not have permission",
            "Your quota allows for 0 more running instance"
        ]

    def slack_color(self) -> str:
        return 'danger'
