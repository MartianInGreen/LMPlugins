import json, urllib, requests, os

def wolframAlpha(query: str):
    # baseURL = f"http://api.wolframalpha.com/v2/query?appid={getEnvVar('WOLFRAM_APP_ID')}&output=json&input="
    baseURL = f"https://www.wolframalpha.com/api/v1/llm-api?appid={os.getenv('WOLFRAM_APP_ID')}&input="

    # Encode the query
    encoded_query = urllib.parse.quote(query)
    url = baseURL + encoded_query

    try:
        response = requests.get(url)
        print(response)
        data = response.text
        print(str(data))
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching Wolfram|Alpha results.')
        }
    
    return {
        'statusCode': 200,
        'results': json.dumps(data)
    }

def api_key_checker(event):
    # See if event["headers"]["x-api-key"] exists
    if "headers" in event:
        if "x-api-key" in event["headers"]:
            if event["headers"]["x-api-key"] == os.getenv("SERVICE_API_KEY"):
                return True
            else:
                print("Token not correct! Token was: " + event["headers"]["x-api-key"])
                return False
        else:
            print("Token not correct! (No token)\n" + str(event["headers"]))
            return False

def lambda_handler(event, context):
    if api_key_checker(event) == False:
        return {
            'statusCode': 401,
            'reason': "Token not correct!"
        }

    try:
        body = event["body"]
        if type(body) == str:
            body = json.loads(body)
    except:
        body = json.loads(event["body"])

    
    if "query" in body:
        query = body["query"]

        return wolframAlpha(query)
    else:
        return {
            'statusCode': 400,
            'reason': "No query provided."
        }