# The simple is just the beginning to open your mind of how everything works in a simple way. "GuiDeLuccaDev"

''' Only one of the methods made available to boto3.
    You can use other information from within the cloudwatch, this is an example.
'''

import boto3
from datetime import datetime, timedelta

class SQS():
    def __init__(self) -> None:
        session = boto3.Session(aws_access_key_id="your_access_key_id",
                            aws_secret_access_key="your_secret_access_key",
                            region_name="your_region_name")

        self.cloudwatch = session.client("cloudwatch")
    
    def get_metrics(self):
        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/SQS',
            MetricName='NumberOfMessagesSent',
            Dimensions=[
                {
                    'Name': 'QueueName',
                    'Value': 'your_name_queue',
                }
            ],
            StartTime=datetime.utcnow() - timedelta(days=3),
            EndTime=datetime.utcnow(),
            Period=86460,
            Statistics=['Average', 'Sum'])
        return str(response)
