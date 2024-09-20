import pandas as pd
import requests
import time

QUERY_TEMPLATES = {
    "Reorganization / Restructuring": [
        "reorganization news",
        "restructuring announcement",
        "consolidation",
        "divestiture news",
        "divestiture timeline"
    ],
    "Mergers and Acquisitions": [
        "acquisition target announcement",
        "acquisition target",
        "merger news",
        "M&A history",
        "acquisition deal closed date"
    ],
    "Top Management Turnover": [
        "CEO resignation announcement",
        "new executive leadership",
        "board of directors change",
        "CFO/COO turnover"
    ],
    "IPO / Financing Rounds": [
        "IPO announcement date",
        "IPO date",
        "series funding",
        "financing rounds",
        "private equity funding"
    ],
    "Name Changes": [
        "rebranding",
        "name change history",
        "name change announcement",
        "renamed to"
    ],
    "Company Events with Other Institutions": [
        "acquisition by [Another Company]",
        "merger with [Another Company]",
        "target in acquisition by [Another Company]",
        "acquiring [Another Company]"
    ]
}


def llama_agent(query_list, message_prompt):
    url = "http://127.0.0.1:5000/api/v1/call_agent"

    payload = {
        "query_list": query_list,
        "llm_payload": {
            "message_prompt": message_prompt,
            "temperature": 0,
            "top_p": 0.1,
            "repetition_penalty": 1.0
        }
    }

    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        return f"Error: {str(e)}"


def create_queries(company_name, event_type):
    queries = [f"{company_name} {query}" for query in QUERY_TEMPLATES.get(event_type, [])]
    return queries

def process_companies_from_excel(input_excel, output_excel):
    df = pd.read_excel(input_excel)
    all_results = []
    
    for index, row in df.iterrows():
        company_name = row['Company Name']
        event_types = QUERY_TEMPLATES.keys()
        
        # Iterate over each event type and generate corresponding queries
        for event_type in event_types:
            queries = create_queries(company_name, event_type)

            message_prompt = [
                {
                    "role": "system",
                    "content": f"You are a smart AI designed to do company research. You have to answer a Main_Question and will be provided Sub_Question queries and their corresponding search results. Based on that you have to form your final answer for main question. Keep responses short and concise."
                },
                {
                    "role": "user",
                    "content": f"Main_Question: Give details on {event_type} for the company {company_name}"
                }
            ]

            result = llama_agent(queries, message_prompt)

            all_results.append({
                'Company Name': company_name,
                'Event Type': event_type,
                'Result': result
            })

            time.sleep(10)

    output_df = pd.DataFrame(all_results)
    output_df.to_excel(output_excel, index=False)
    print(f"Results written to {output_excel}")

input_excel = 'company_list.xlsx'
output_excel = 'company_event_results.xlsx'
process_companies_from_excel(input_excel, output_excel)
