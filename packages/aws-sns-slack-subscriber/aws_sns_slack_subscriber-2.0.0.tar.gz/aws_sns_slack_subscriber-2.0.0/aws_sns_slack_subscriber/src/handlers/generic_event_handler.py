from typing import Tuple, Optional

try:
    from aws_sns_slack_subscriber.src.handlers.base_event_handler import BaseEventHandler
except ImportError:
    # noinspection PyUnresolvedReferences
    from handlers.base_event_handler import BaseEventHandler


class GenericEventHandler(BaseEventHandler):
    def my_source(self) -> str:
        return '*'

    def generate_response(self) -> Tuple[Optional[str], Optional[str]]:
        return (
            self.event_message['source'],
            f'{self.event_message["time"]}: {self.event_message["detail"]}'
        )
