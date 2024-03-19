import subprocess, os, json, uuid, re
import io, contextlib
import boto3 
import IPython

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

    try:
        code = body["code"]
    except:
        return {
            'statusCode': 400,
            'reason': "No code provided."
        }
    
    print("code: " + code)
    
    try:
        packages = body["packages"]
        print("packages: " + packages)
    except:
        packages = None

    # Create a new StringIO object
    print("Creating a new StringIO object")
    buffer = io.StringIO()

    # Redirect stdout to the buffer
    with contextlib.redirect_stdout(buffer):
        os.chdir("./tmp")
        IPython.start_ipython(argv=['-c', f'{code}'])

    # Get the contents of the buffer
    try: 
        output = buffer.getvalue()
        output = re.sub(r'\x1b\[.*?[@-~]|\x1b].*?\x07', '', output)

        if output == "" or output == None:
            output = "No output"
    except:
        output = "No output"

    return_output = {
        'output': output
    }

    print(return_output)

    return return_output

if __name__ == "__main__":
    os.environ["SERVICE_API_KEY"] = "test"

    event = {
        "headers": {
            "x-api-key": os.getenv("SERVICE_API_KEY")
        },
        "body": {
            "code": "from matplotlib import pyplot as plt\nplot = plt.plot([1, 2, 3, 4])\nplot.save('test.png')",
        }
    }

    lambda_handler(event, None)