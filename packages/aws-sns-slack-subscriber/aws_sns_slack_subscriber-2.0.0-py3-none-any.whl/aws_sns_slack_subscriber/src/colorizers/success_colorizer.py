from typing import List

try:
    from aws_sns_slack_subscriber.src.colorizers.base_colorizer import BaseColorizer
except ImportError:
    # noinspection PyUnresolvedReferences
    from colorizers.base_colorizer import BaseColorizer


class SuccessColorizer(BaseColorizer):
    def __init__(self, message: str):
        super().__init__(message)

    def matches(self) -> List[str]:
        return ['*']

    def slack_color(self) -> str:
        return 'good'
