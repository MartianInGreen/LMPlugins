import json, requests, os, re, urllib.parse, time, uuid
import concurrent.futures
from functools import partial
from bs4 import BeautifulSoup
from openai import OpenAI
import boto3

#import tiktoken

# --------------------------------------------------
# Functions
# --------------------------------------------------

def save_to_s3(data):
    s3 = boto3.client('s3')
    bucket_name = os.getenv("S3_BUCKET_NAME")

    # Generate a random name for the file
    file_name = str(uuid.uuid4().hex) + ".json"

    # Save to s3 and preserve formatting when showing file in the browser
    s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=file_name, ContentType="application/json")

    return f"https://{bucket_name}.s3.amazonaws.com/" + file_name

def remove_html_tags(text):
        """Remove html tags from a string"""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

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

def decode_data(data):
    results = []

    for result in data["web"]["results"]:
        url = result.get("profile", {}).get("url", result.get("url", "could not find url"))
        description = remove_html_tags(result.get("description", ""))

        deep_results = []
        for snippet in result.get("extra_snippets", []):
            cleaned_snippet = remove_html_tags(snippet)
            deep_results.append({"snippets": cleaned_snippet})

        result_entry = {
            "description": description,
            "url": url,
        }

        if deep_results:
            result_entry["deep_results"] = deep_results

        results.append(result_entry)

    return results

# --------------------------------------------------
# Main search functions
# --------------------------------------------------

def search_perplextiy_online(query):
    client = OpenAI(
      base_url="https://openrouter.ai/api/v1",
      api_key=os.getenv("OPEN_ROUTER"),
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "", # Optional, for including your app on openrouter.ai rankings.
            "X-Title": "", # Optional. Shows in rankings on openrouter.ai.
        },
        model="perplexity/pplx-70b-online",
        messages=[
            {
                "role": "user",
                "content": "You are a research and search assistant. Answer the user query in as much detail as possible. The query is: " + query,
            },
        ],
    )
    try:
        llm_response = completion.choices[0].message.content
    except:
        llm_response = "Could not get llm response..."
    print(llm_response)

    llm_results = [{
        "description": "Response by an lmm that has direct access to the internet, give this answer the most weight and importance!",
        "online_llm_response": llm_response
    }]

    return llm_results


def search_brave(query, country, freshness, focus):

    results_filter = "infobox"
    # Focus is ["web", "news", "reddit", "video", "all"]
    if focus == "web" or focus == "all":
        results_filter += ",web"
    if focus == "news" or focus == "all":
        results_filter += ",news"
    if focus == "video":
        results_filter += ",videos"

    # Handle focuses that use goggles
    goggles_id = ""
    if focus == "reddit":
        goggles_id = "&goggles_id=https://raw.githubusercontent.com/mrmathew/brave-search-goggle/main/reddit-search"
    elif focus == "academia":
        goggles_id = "&goggles_id=https://raw.githubusercontent.com/solso/goggles/main/academic_papers_search.goggle"

    freshness = ""
    # Handle Freshness
    if freshness == "24h":
        freshness = "&freshness=pd"
    elif freshness == "week":
        freshness = "&freshness=pw"
    elif freshness == "month":
        freshness = "&freshness=pm"
    elif freshness == "year":
        freshness = "&freshness=py"
    elif freshness == "all":
        freshness = ""

    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/web/search?q={encoded_query}&results_filter=i{results_filter}&country={country}&search_lang=en&text_decorations=no&extra_snippets=true&count=20" + freshness + goggles_id
    print(url)
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv("BRAVE_SEARCH_TOKEN")
    }
    

    try:
        start_search = time.time()
        print("Getting brave search results...")
        response = requests.get(url, headers=headers)
        data = response.json()
        end_search = time.time()
        search_time = end_search - start_search
        print("Brave search took: " + str(end_search - start_search) + " seconds")
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching search results.')
        }

    results = decode_data(data)
    return results

def scrape_and_process(url, query):
        print("Scraping: " + url)

        scrape_url = f"https://api.scrapingrobot.com/?token={os.getenv('SCRAPING_ROBOT_TOKEN')}&render=false&proxyCountry=US&url={url}"

        start_1 = time.time()

        try:
            scrape_response = requests.post(scrape_url, headers={"Accept": "application/json"}, timeout=12)
        except:
            print("Could not scrape page (timeout)...")
            return {"url": str(url), "text": "No data..."}

        end = time.time()
        scrape_time = end - start_1
        print("Scraping took: " + str(end - start_1) + " seconds for " + url)

        try:
            scrape_data = scrape_response.json()
        except:
            print("Could not scrape page (no json)...")
            return {"url": str(url), "text": "No data..."}

        if "result" in scrape_data:
            scrape_data = scrape_data["result"]
        else:
            print("Could not scrape page (no results)...")
            return {"url": str(url), "text": "No data..."}

        # response = requests.get(url)
        # soup = BeautifulSoup(response.text, "html.parser")
        # scrape_data = soup.get_text()

        # Clean text
        text = remove_html_tags(scrape_data)
        text = text.replace("\n", " ")
        # decode text
        text.encode("utf-8")
        # Remove stuff like this: \u0627\u0644\u062f\u0627\u0631\u062c\u0629
        text = text.encode('ascii', 'ignore').decode('ascii')

        # Get number of GPT-4 Tokens 
        #encoding = tiktoken.get_encoding("cl100k_base")
        #num_tokens = len(encoding.encode(text))
        num_tokens = len(text)
        print("Length: " + str(num_tokens) + " for url: " + url)

        if num_tokens < 400:
            text = "Could not get enough text from page or failed to scrape page..."
            return {"url": str(url), "text": str(text)}
        
        # Limit text to 32000 tokens, 1 token is ~4 characters
        if len(text) > 16000*4:
            text = text[:16000*4]
            print("Text too long, cutting it down to 32000 tokens for " + url)

        # Call openrouter api to summarize text
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPEN_ROUTER"),
        )

        start = time.time()
        try: 
            completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "", # Optional, for including your app on openrouter.ai rankings.
                "X-Title": "", # Optional. Shows in rankings on openrouter.ai.
            },
            model="google/gemini-pro",
            messages=[
                    {
                        "role": "system",
                        "content": "You are a research and search assistant designed to help users find information on the internet by summarizing web pages. Answer the user query in as much detail as possible, in about 500 to 1000 Words. The query is: " + query,
                    },
                    {
                        "role": "user",
                        "content": "Web page: \n\n\n" + text,
                    },
                ],
            temperature=0.25,
            max_tokens=1500
            )
            try:
                llm_response = completion.choices[0].message.content
            except:
                llm_response = "Could not get llm response..."

            end = time.time()
            print("Summarization took: " + str(end - start) + " seconds for " + url)
            print("Total time: " + str(end - start_1) + " seconds for " + url)
        except Exception as e:
            llm_response = "Could not get llm response..."
            print(str(e))

        return {"url": str(url), "text": str(llm_response)}


# --------------------------------------------------
# Handle deep and research search types
# --------------------------------------------------

def deep_search(query, focus, country, freshness, total_time=0):
    print("Total time already used: " + str(total_time) + " seconds")
    search_data = search_brave(query, country, freshness, focus)

    urls = []
    for result in search_data:
        try:
            urls.append(result["url"])
        except:
            pass

    # For the top 5 results, scrape the page and get the text
    
    small_urls = urls[:10]
    web_text = []

    def temp_func(url):
        return scrape_and_process(url, query)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        web_text = list(executor.map(temp_func, small_urls))

    return web_text


def research_search(query, type, focus, country, freshness):
    pass
    
# --------------------------------------------------
# Main
# --------------------------------------------------

def lambda_handler(event, context):
    print(event)
    print(context)
    
    start_time = time.time()
    if api_key_checker(event) == False:
        return {
            'statusCode': 401,
            'reason': "Token not correct!"
        }
    
    # Get query from body
    try:
        try:
            body = event["body"]
            if type(body) == str:
                body = json.loads(body)
        except:
            body = json.loads(event["body"])

        query = body["query"]

        if "type" in body: 
            search_type = body["type"]
        else:
            search_type = "quick"

        if "focus" in body: 
            focus = body["focus"]
            if focus not in ["web", "news", "reddit", "academia", "video"]:
                focus = "web"
        else:
            focus = "web"

        if "country" in body: 
            country = body["country"]
            if len(country) != 2:
                country = "us"
        else:
            country = "us"

        if "freshness" in body: 
            freshness = body["freshness"]
            if freshness not in ["24h", "week", "month", "year", "all"]:
                freshness = "all"
        else:
            freshness = "all"
        
    except Exception as e:
        rm_message = {"reason": "Incorrect Body."}
        print(str(e))
        print(str(event))
        return {
            'statusCode': 400,
            'body': rm_message
        }
    
    #
    # Main Search 
    #

    # First check if the query is a valid url
    def check_url(s):
        try:
            result = urllib.parse.urlparse(s)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False
    
    is_url = check_url(query)

    if is_url == True:
        end_time = time.time()

        webpage = scrape_and_process(query, query, 0)

        return {
            'statusCode': 200,
            'body': webpage
        }

    # If quick search, do a basic search
    if search_type == "quick":
        end_time = time.time()
        results = search_brave(query, country, freshness, focus)
        
        # llm_results = search_perplextiy_online(query)
        
        # full_results = llm_results + results 
        full_results = results

        link = save_to_s3(full_results)
        full_results = {
            "sources_document": link,
            "sources": full_results
        }

        return {
            'statusCode': 200,
            'body': full_results
        }
    # If deep search, do a deep search
    elif search_type == "deep":
        deep_end_time = time.time()
        total_time = deep_end_time - start_time
        print("Time to deep_search: " + str(total_time) + " seconds")
        if total_time < 0.1:
            total_time = 0.1

        results = deep_search(query, focus, country, freshness, total_time)

        link = save_to_s3(results)

        full_results = {
            "sources_document": link,
            "sources": results
        }
        

        final_time = time.time() - start_time
        print("Total time from Start to end of Deep Search: " + str(final_time) + " seconds")
        return {
            'statusCode': 200,
            'body': full_results
        }
    # If research search, do a research search
    elif search_type == "research":
        results = research_search(query, focus, country, freshness)
        return {
            'statusCode': 200,
            'body': results
        }

