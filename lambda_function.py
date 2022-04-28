import yfinance as yf
import boto3
import uuid
import io

def lambda_handler(event, context):
    if "ticker" in event:
        client = boto3.client('kinesis')

        stockData = yf.download(event['ticker'], period=event['period'], interval=event['interval'])
        # stockData = yf.download(event['ticker'], period="2y", interval="1h")
        stockData['ticker'] = event['ticker']
        stockData['period'] = event['period']
        stockData['interval'] = event['interval']
        response = client.put_record(
                StreamName='stocks',
                Data=stockData.to_json(),
                PartitionKey=str(uuid.uuid4())
            )
        return response
            
        # with io.StringIO() as csv_buffer:
        #     stockData.to_csv(csv_buffer)
        #     response = client.put_record(
        #         StreamName='stocks',
        #         Data=csv_buffer.getvalue(),
        #         PartitionKey=str(uuid.uuid4())
        #     )
        #     return response
    else:
        return "Send a ticker"


# docker build -t stocks-info . 
# docker tag stocks-info:latest 670836484442.dkr.ecr.us-east-1.amazonaws.com/stocks-info:latest 
# docker push 670836484442.dkr.ecr.us-east-1.amazonaws.com/stocks-info:latest 
