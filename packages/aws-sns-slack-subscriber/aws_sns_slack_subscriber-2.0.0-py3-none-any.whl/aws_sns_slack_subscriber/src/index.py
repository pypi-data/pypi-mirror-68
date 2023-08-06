import json
import os
import urllib3

from json import JSONDecodeError
from typing import Any, Dict, List, Type

try:
    from aws_sns_slack_subscriber.src.colorizers.base_colorizer import BaseColorizer
    from aws_sns_slack_subscriber.src.colorizers.error_colorizer import ErrorColorizer
    from aws_sns_slack_subscriber.src.colorizers.success_colorizer import SuccessColorizer
    from aws_sns_slack_subscriber.src.colorizers.warning_colorizer import WarningColorizer
    from aws_sns_slack_subscriber.src.handlers.base_event_handler import BaseEventHandler
    from aws_sns_slack_subscriber.src.handlers.generic_event_handler import GenericEventHandler
    from aws_sns_slack_subscriber.src.handlers.pipeline_event_handler import PipelineEventHandler
except ImportError:
    # noinspection PyUnresolvedReferences
    from colorizers.base_colorizer import BaseColorizer
    # noinspection PyUnresolvedReferences
    from colorizers.error_colorizer import ErrorColorizer
    # noinspection PyUnresolvedReferences
    from colorizers.success_colorizer import SuccessColorizer
    # noinspection PyUnresolvedReferences
    from colorizers.warning_colorizer import WarningColorizer
    # noinspection PyUnresolvedReferences
    from handlers.base_event_handler import BaseEventHandler
    # noinspection PyUnresolvedReferences
    from handlers.generic_event_handler import GenericEventHandler
    # noinspection PyUnresolvedReferences
    from handlers.pipeline_event_handler import PipelineEventHandler

HANDLERS: List[Type[BaseEventHandler]] = [
    PipelineEventHandler,
    GenericEventHandler
]

COLORIZERS: List[Type[BaseColorizer]] = [
    WarningColorizer,
    ErrorColorizer,
    SuccessColorizer
]


def handler(event: Dict[str, Any], context: Any) -> None:
    print(f'Event received: {json.dumps(event)}.')

    for record in event['Records']:
        sns = record.get('sns', record.get('Sns', record.get('SNS'))) or {}

        message = sns.get('Message') or '<-no-message->'
        colorizers = [colorizer(message) for colorizer in COLORIZERS]
        color = None

        for colorizer in colorizers:
            color = colorizer.match()

            if color:
                break

        title = sns.get('Subject', 'SNS') or 'aws:sns'
        subtitle = message
        color = color or 'good'

        try:
            message = json.loads(message)
            handlers = [handler(message) for handler in HANDLERS]

            for handler in handlers:
                if handler.my_source() == '*':
                    title, subtitle = handler.generate_response()
                    break
                elif handler.event_source == handler.my_source():
                    title, subtitle = handler.generate_response()
                    break
        except (TypeError, JSONDecodeError):
            pass

        post_data = {
            "channel": os.environ['SLACK_CHANNEL'],
            "username": 'Amazon Web Services',
            "text": "*" + title + "*",
            "icon_emoji": ":arrow_forward:",
            "attachments": [{
                "color": color,
                "text": subtitle
            }]
        }

        encoded_body = json.dumps(post_data)

        http = urllib3.PoolManager()

        r = http.request(
            method='POST',
            url=os.environ['SLACK_WEBHOOK_URL'],
            headers={'Content-Type': 'application/json'},
            body=encoded_body
        )

        print(r.read())
