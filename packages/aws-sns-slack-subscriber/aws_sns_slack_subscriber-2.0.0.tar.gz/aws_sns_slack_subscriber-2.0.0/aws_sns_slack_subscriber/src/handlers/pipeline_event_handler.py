from typing import Tuple, Optional

try:
    from aws_sns_slack_subscriber.src.handlers.base_event_handler import BaseEventHandler
except ImportError:
    # noinspection PyUnresolvedReferences
    from handlers.base_event_handler import BaseEventHandler


class PipelineEventHandler(BaseEventHandler):
    def my_source(self) -> str:
        return 'aws.codepipeline'

    def generate_response(self) -> Tuple[Optional[str], Optional[str]]:
        time: str = self.event_message["time"]
        time = time.replace('T', ' ').replace('Z', '')

        return (
            self.event_message['detail']['pipeline'],
            f'{time}: {self.event_message["detail"]["state"]}'
        )
