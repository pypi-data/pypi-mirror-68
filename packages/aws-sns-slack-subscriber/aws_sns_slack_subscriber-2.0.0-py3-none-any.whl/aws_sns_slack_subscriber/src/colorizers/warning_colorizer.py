from typing import List

try:
    from aws_sns_slack_subscriber.src.colorizers.base_colorizer import BaseColorizer
except ImportError:
    # noinspection PyUnresolvedReferences
    from colorizers.base_colorizer import BaseColorizer


class WarningColorizer(BaseColorizer):
    def __init__(self, message: str):
        super().__init__(message)

    def matches(self) -> List[str]:
        return [
            "aborted operation.",
            "to YELLOW",
            "Adding instance ",
            "Degraded to Info",
            "Deleting SNS topic",
            "is currently running under desired capacity",
            "Ok to Info",
            "Ok to Warning",
            "Pending Initialization",
            "Removed instance ",
            "Rollback of environment"
        ]

    def slack_color(self) -> str:
        return 'warning'
