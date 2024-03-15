# TypingMind Plugins

These are (most of) my TypingMind Plugins, I've decided to make them OpenSource for anyone to use who wants them. 

# General

All plugins are designed to have a AWS Lambda Python function part and a simple wrapper for calling the Lambda function on the TypingMind side.

**Installation**

1. Create an AWS account (you can do this for free, you get a lot of AWS Lambda function calls completly free each month)
2. Create a lambda function
   1. Give it a name that is easily identifiable 
   2. Set the runtime to Python (preferably 3.10 or 3.11 both should work)
   3. Under advanced settings click Enable function URL 
   4. Set Auth type to None (We'll have own custom auth in most plugins, however be aware that this makes your functions publicly accessible in theory)
   5. Enable "Configure cross-origin resource sharing (CORS)"
3. Configure lambda function
   1. Go to configuration/General -> Set timeout according to each function (you can probably just set this to around 1m)
   2. Go to configuration/Function URL and click on edit
      1. Set allow Origin to * (or you can set it to the typingmind domain)
      2. Add x-api-key, access-control-allow-origin, and content-type to "Expose headers" and "Allow headers"
      3. Under Allow methods add *
      4. Enable Allow credentials
   3. Go to configuration/Environment variables -> Set your API Keys and set the "SERVICE_API_KEY" to what you want your API key to be
4. Copy the python code to your functions lambda_function.py
5. Look under the plugin header below which packages are needed for the plugin
   1. Open a Linux Terminal (Under WSL or native)
   2. Create a folder `mkdir python`
   3. Run `python3 -m pip install package_1 package_2 --target ./`
   4. Zip the folder `cd .. && zip -r my-lambda-layer.zip python`
   5. Create a new Layer on AWS, select the python version and upload your ZIP file
6. Copy your function URL 
7. Create a new Plugin on Typingmind
8. Copy the respective plugin-name.json to the OpenAI function spec
9. Copy the respective plugin-name.js to the Code Implementation and replace with your function URL and API Key  
10. And you're done!

# Plugins

## YouTube

A simple YouTube transcript getter, useful for Video Summarization etc. 

**Installation**
- Packages: youtube_transcript_api

## Pondera 

An in-depth LLM search engine with multiple modes. 

**Installation**
- Packages: bs4, requests, re, openai, boto3
- Set your "OPEN_ROUTER" API key
- Set your "BRAVE_SEARCH_TOKEN" API key 
- Set your "SCRAPING_ROBOT_TOKEN" API key

## Wolfram

A simple Wolfram|Alpha llm api wrapper

**Installation**
- Packages: requests
- Set your "WOLFRAM_APP_ID" API key

## imageGen

Wrapper for multiple ImageGen models. 

**Installation**
- Packages: replicate, requests, openai
- Set your "OPENAI_API_KEY"
- Set your "REPLICATE_API_KEY"