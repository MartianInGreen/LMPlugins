import subprocess, os, json, uuid, re
import io, contextlib
import boto3 
import IPython
from IPython.core.interactiveshell import InteractiveShell
import textwrap

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
    
    try:
        packages = body["packages"]
        print("packages: " + packages)
    except:
        packages = None

    # Create a new StringIO object
    buffer = io.StringIO()

    # Redirect stdout to the buffer
    try:
        print("Starting Code Execution")
        os.environ['IPYTHONDIR'] = '/tmp'

        print("code: \n" + code)

        shell = InteractiveShell.instance()

        with contextlib.redirect_stdout(buffer):
            try:
                result = shell.run_cell(code)
                if result.error_in_exec is not None:
                    output = "IPython execution error: " + str(result.error_in_exec)
                    print(output)
                    return {
                        'output': output
                    }
            except SystemExit as e:
                output = "IPython execution exited with code: " + str(e.code)
                print(output)
                return {
                    'output': output
                }
            
        print("Got code results")
    
        # Get the contents of the buffer
        output = buffer.getvalue()
        output = re.sub(r'\x1b\[.*?[@-~]|\x1b].*?\x07', '', output)
        print("Parsed code results")
    except Exception as e:
        print(e)
        output = buffer.getvalue()

    return_output = {
        'output': output
    }

    print(return_output)

    return return_output