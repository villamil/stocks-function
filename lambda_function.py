import yfinance as yf
import boto3
import uuid
import requests
import os


def lambda_handler(event, context):
    if "symbol" in event and "interval" in event:
        client = boto3.client('kinesis')

        apikey = os.environ['API_KEY']

        req = requests.get('https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&format=CSV&apikey={apikey}'.format(
            symbol=event['symbol'], interval=event['interval'], apikey=apikey))
        url_content = req.content
        response = client.put_record(
            StreamName='stocks',
            Data=url_content,
            PartitionKey=str(uuid.uuid4())
        )
        return response
    else:
        return "Send a symbol and an interval"
