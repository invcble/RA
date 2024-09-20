import requests, os, json
from dotenv import load_dotenv
load_dotenv()



def google_search(query):
    api_key = os.getenv('GOOGLE_SEARCH_API')
    cse_id = os.getenv('CSE_ID')
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={query}"
    response = requests.get(url, )

    result = response.json()
    # print(result)
    
    try:
        snippets = ' \n\n| '.join([str({"title":item['title'], "snippet": item['snippet'], "link": item['link']}) for item in result['items']])
    except KeyError:
        snippets = 'No results found for this search.'

    # with open("response-google-api.json", 'w') as f:
    #         json.dump(result, f, indent=4)

    return snippets

# print(google_search("Temp at kolkata now"))
# print(google_search("WEG Corporate Vietnam manufacturing warehousing assembly presence"))