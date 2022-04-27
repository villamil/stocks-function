import yfinance as yf
import boto3
import uuid
import io

def lambda_handler(event, context):
    return "hello there"
    if "ticker" in event:
        client = boto3.client('kinesis')

        stockData = yf.download(event['ticker'], period="1y")
        # stockData = yf.download(event['ticker'], period="2y", interval="1h")

        with io.StringIO() as csv_buffer:
            stockData.to_csv(csv_buffer, index=False)
            response = client.put_record(
                StreamName='stocks',
                Data=csv_buffer.getvalue(),
                PartitionKey=str(uuid.uuid4())
            )
            return response
    else:
        return "Send a ticker"


# docker build -t stocks-info . 
# docker tag stocks-info:latest 670836484442.dkr.ecr.us-east-1.amazonaws.com/stocks-info:latest 
# docker push 670836484442.dkr.ecr.us-east-1.amazonaws.com/stocks-info:latest 
