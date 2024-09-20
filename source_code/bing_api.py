import os, json
import requests
from dotenv import load_dotenv

load_dotenv()

subscription_key = os.getenv('BING_SEARCH_V7_SUBSCRIPTION_KEY')
endpoint = "https://api.bing.microsoft.com/v7.0/search"

def bing_search(query):
    params = {'q': query, 'mkt': 'en-US', 'count': 6}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}

    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        search_results = response.json()

        output = "SEARCH RESULTS : \n"
        for result in search_results.get('webPages', {}).get('value', []):
            output += f"Title: {result.get('name', 'No title')}\n"
            output += f"Snippet: {result.get('snippet', 'No snippet')}\n"
            output += f"URL: {result.get('url', 'No URL')}\n\n"

        if not output:
            output = "No relevant search results found."

        # with open("response-bing-api.json", 'w') as f:
        #     json.dump(search_results, f, indent=4)

    except requests.exceptions.RequestException as e:
        output = f"Error occurred: {e}"
    
    return output

# print(bing_search("Temp at kolkata now"))
# print(bing_search("Dril-quip India office"))