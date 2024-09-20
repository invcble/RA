import requests, os, time
from dotenv import load_dotenv
load_dotenv()



def brave_search(query):
    time.sleep(1)

    api_key = os.getenv('BRAVE_SEARCH_API')
    url = f"https://api.search.brave.com/res/v1/web/search?q={query}&count=5"
    headers = {
        "Accept": "application/json",
        "Accept-Encoding": "gzip",
        "X-Subscription-Token": api_key
    }
    
    response = requests.get(url, headers=headers)
    result = response.json()
    # print(result)
    snippets = ''
    
    for item in result['web']['results']:
        try:
            snippets += str({"title":item['title'], "snippet": item['description'], "link": item['url'], "AI_snippet": item['extra_snippets']}).replace("</strong>", '').replace("<strong>", '')
        except:
            snippets += str({"title":item['title'], "snippet": item['description'], "link": item['url']}).replace("</strong>", '').replace("<strong>", '')
        snippets += ' \n\n| '
    
    return snippets


# print(brave_search("WEG Corporate India Office"))
# print(brave_search('melling.com India address'))