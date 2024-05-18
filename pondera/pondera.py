import json
import os
import re
import urllib.parse
import time
import uuid
import concurrent.futures
import requests
from bs4 import BeautifulSoup
from openai import OpenAI
import boto3

# --------------------------------------------------
# Helper Functions
# --------------------------------------------------

def save_to_s3(data):
    """
    Save data to an S3 bucket and return the public URL.

    Args:
        data (dict): Data to be saved as a JSON file.

    Returns:
        str: Public URL of the saved file.
    """
    s3 = boto3.client('s3')
    bucket_name = os.getenv("S3_BUCKET_NAME")

    # Generate a random name for the file
    file_name = str(uuid.uuid4().hex) + ".json"

    # Save to S3 and preserve formatting when showing file in the browser
    s3.put_object(Body=json.dumps(data), Bucket=bucket_name, Key=file_name, ContentType="application/json")

    return f"https://{bucket_name}.s3.amazonaws.com/" + file_name


def remove_html_tags(text):
    """
    Remove HTML tags from a string.

    Args:
        text (str): Input text possibly containing HTML tags.

    Returns:
        str: Text with HTML tags removed.
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def api_key_checker(event):
    """
    Check if the API key in the request headers matches the expected key.

    Args:
        event (dict): Event data containing request headers.

    Returns:
        bool: True if the API key is correct, False otherwise.
    """
    if "headers" in event and "x-api-key" in event["headers"]:
        if event["headers"]["x-api-key"] == os.getenv("SERVICE_API_KEY"):
            return True
        else:
            print("Token not correct! Token was: " + event["headers"]["x-api-key"])
            return False
    else:
        print("Token not correct! (No token)\n" + str(event["headers"]))
        return False


def decode_data(data):
    """
    Extract relevant information from the search API response.

    Args:
        data (dict): Response data from the search API.

    Returns:
        list: List of dictionaries containing the extracted information.
    """
    results = []

    try:
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
    except Exception as e:
        print(str(e))
        return ["No search results from Brave (or an error occured)..."]


# --------------------------------------------------
# Search Functions
# --------------------------------------------------

def search_perplextiy_online(query):
    """
    Search using the Perplexity online model.

    Args:
        query (str): Search query.

    Returns:
        list: List containing the model's response.
    """
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER"),
    )

    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "",  # Optional, for including your app on openrouter.ai rankings.
            "X-Title": "",  # Optional. Shows in rankings on openrouter.ai.
        },
        model="perplexity/llama-3-sonar-large-32k-online",
        max_tokens=500,
        messages=[
            {
                "role": "user",
                "content": str(query),
            },
        ],
    )

    try:
        llm_response = completion.choices[0].message.content
    except:
        llm_response = "Could not get llm response..."

    print(llm_response)

    return [{"description": "Response by an lmm that has direct access to the internet, give this answer the most weight and importance!",
             "online_llm_response": llm_response}]


def search_brave(query, country, freshness_raw, focus, search_perplexity = False):
    """
    Search using the Brave Search API.

    Args:
        query (str): Search query.
        country (str): Two-letter country code.
        freshness (str): Filter search results by freshness (e.g., '24h', 'week', 'month', 'year', 'all').
        focus (str): Focus the search on specific types of results (e.g., 'web', 'news', 'reddit', 'video', 'all').

    Returns:
        list: List of dictionaries containing search results.
    """
    results_filter = "infobox"
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
    if freshness_raw != None and freshness_raw in ["24h", "week", "month", "year"]:
        # Map freshness to ["pd", "pw", "pm", "py"] / No freshness for "all"
        freshness_map = {
            "24h": "pd",
            "week": "pw",
            "month": "pm",
            "year": "py",
        }

        freshness = freshness_map[freshness_raw]

        freshness = f"&freshness={freshness}"

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
        print("Brave search took: " + str(end_search - start_search) + " seconds")
    except:
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching search results.')
        }

    results = decode_data(data)
    return results


def scrape_and_process(url, query):
    """
    Scrape and process a web page.

    Args:
        url (str): URL of the web page to scrape.
        query (str): Search query for which the web page is being processed.

    Returns:
        dict: Dictionary containing the URL and a summary of the web page content.
    """
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

    # Clean text
    text = remove_html_tags(scrape_data)
    text = text.replace("\n", " ")
    try:
        text = text.encode("utf-8")
        #text = text.encode('ascii', 'ignore').decode('ascii')

        # Clean text
        text = text.decode("utf-8")
    except:
        print("Could not encode text...")
        text = "Could not encode text..."
        return {"url": str(url), "text": str(text)}

    num_tokens = len(text)
    print("Length: " + str(num_tokens) + " for url: " + url)

    if num_tokens < 400:
        text = "Could not get enough text from page or failed to scrape page..."
        return {"url": str(url), "text": str(text)}

    # Limit text to 32000 tokens, 1 token is ~4 characters
    if len(text) > 16000 * 4:
        text = text[:16000 * 4]
        print("Text too long, cutting it down to 16000 * 4 characters for " + url)

    # Call openrouter api to summarize text
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPEN_ROUTER"),
    )

    start = time.time()
    try:
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "",  # Optional, for including your app on openrouter.ai rankings.
                "X-Title": "",  # Optional. Shows in rankings on openrouter.ai.
            },
            model="anthropic/claude-3-haiku:beta",
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


def deep_search(query, focus, country, freshness, total_time=0):
    """
    Perform a deep search by scraping and summarizing the top search results.

    Args:
        query (str): Search query.
        focus (str): Focus the search on specific types of results (e.g., 'web', 'news', 'reddit', 'video', 'all').
        country (str): Two-letter country code.
        freshness (str): Filter search results by freshness (e.g., '24h', 'week', 'month', 'year', 'all').
        total_time (float): Total time already spent on the search (in seconds).

    Returns:
        list: List of dictionaries containing summaries of the scraped web pages.
    """
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

def search_images_and_video(query, country, type, freshness = None):
    encoded_query = urllib.parse.quote(query)
    url = f"https://api.search.brave.com/res/v1/{type}/search?q={encoded_query}&country={country}&search_lang=en&count=10"

    if freshness != None and freshness in ["24h", "week", "month", "year"] and type == "videos":
        # Map freshness to ["pd", "pw", "pm", "py"] / No freshness for "all"
        freshness_map = {
            "24h": "pd",
            "week": "pw",
            "month": "pm",
            "year": "py",
        }

        freshness = freshness_map[freshness]

        url += f"&freshness={freshness}"

    print(url)

    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": os.getenv("BRAVE_SEARCH_TOKEN")
    } 

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        #return data
        #print(json.dumps(data, indent=2))
        
        if type == "images":
            formatted_data = {}
            for i, result in enumerate(data["results"], start=1):
                print(result)
                formatted_data[f"image{i}"] = {
                    "source": result["url"],
                    "page_fetched": result["page_fetched"],
                    "title": result["title"],
                    "image_url": result["properties"]["url"]
                }
            
            return formatted_data
        else: 
            return data
    except Exception as e:
        print(e)
        return {
            'statusCode': 400,
            'body': json.dumps('Error fetching search results.')
        }

def search_local():
    pass

def lambda_handler(event, context):
    """
    AWS Lambda function handler for search requests.

    Args:
        event (dict): Event data containing the request information.
        context (object): Context object containing information about the Lambda environment.

    Returns:
        dict: Response dictionary with the search results or an error message.
    """
    print(event)
    print(context)

    start_time = time.time()
    if not api_key_checker(event):
        return {
            'statusCode': 401,
            'reason': "Token not correct!"
        }

    # Get query and search parameters from the request body
    try:
        try: 
            body = json.loads(event["body"])
        except:
            body = event["body"]
        query = body["query"]

        search_type = body.get("type", "quick")
        focus = body.get("focus", "web")
        if focus not in ["web", "news", "reddit", "academia"]:
            focus = "web"

        country = body.get("country", "us")
        if len(country) != 2:
            country = "us"

        freshness = body.get("freshness", "all")
        if freshness not in ["24h", "week", "month", "year", "all"]:
            freshness = "all"

        if search_type not in ["quick", "deep", "images", "videos"]:
            search_type = "quick"

    except Exception as e:
        rm_message = {"reason": "Incorrect Body."}
        print(str(e))
        print(str(event))
        return {
            'statusCode': 400,
            'body': rm_message
        }

    # Check if the query is a valid URL
    def check_url(s):
        try:
            result = urllib.parse.urlparse(s)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    is_url = check_url(query)

    if is_url:
        end_time = time.time()
        webpage = scrape_and_process(query, "Summarize this webpage in detail!")

        return {
            'statusCode': 200,
            'body': webpage
        }

    # Perform the requested search type
    if search_type == "quick":
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.submit(search_brave, query, country, freshness, focus)
            perplexity = executor.submit(search_perplextiy_online, query)

        results = results.result()
        perplexity = perplexity.result()
        full_results = perplexity + results

        link = save_to_s3(full_results)
        full_results = {
            "sources_document": link,
            "sources": full_results
        }

        return {
            'statusCode': 200,
            'body': full_results
        }

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

    elif search_type == "research":
        return {
            'statusCode': 501,
            'body': "Research search type not implemented."
        }
    
    elif search_type == "videos" or search_type == "images":      
        data = search_images_and_video(query, country, search_type, freshness)
        return {
            'statusCode': 200,
            'body': data
        }
