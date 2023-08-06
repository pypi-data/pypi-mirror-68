from aws_cdk import aws_lambda
from aws_cdk.aws_sns import ITopic
from aws_cdk.aws_sns_subscriptions import LambdaSubscription
from aws_cdk.core import Stack
from aws_sns_slack_subscriber import root_path


class SlackSubscriber(aws_lambda.Function):
    def __init__(
            self,
            scope: Stack,
            id: str,
            slack_webhook_url: str,
            slack_channel: str,
            sns_topic: ITopic
    ) -> None:
        """
        Constructor.

        :param scope: A Cloud formation stack to which this resource will be added.
        :param id: Resource id.
        :param slack_webhook_url: Slack webhook url to post callbacks.
        :param slack_channel: A channel to which send the post. Usually looks like this: "#aws-sns-channel".
        :param sns_topic: A SNS Topic to which this lambda should be subscribed.
        """
        super().__init__(
            scope,
            id,
            code=aws_lambda.Code.from_asset(f'{root_path}/src'),
            handler='index.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            environment={
                'SLACK_WEBHOOK_URL': slack_webhook_url,
                'SLACK_CHANNEL': slack_channel
            }
        )

        # noinspection PyTypeChecker
        sns_topic.add_subscription(LambdaSubscription(self))
