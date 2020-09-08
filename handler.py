import json
import syncBots


def syncBots(event, context):

    output = syncBots.run()
    
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event + output
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY
    # integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


if __name__ == "__main__":
    syncBots('', '')
