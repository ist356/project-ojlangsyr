import requests
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

GAMMA_API_BASE_URL = "https://gamma-api.polymarket.com"

def fetch_all_markets():
    endpoint = f"{GAMMA_API_BASE_URL}/markets"
    all_markets = []
#pagination start
    limit = 100
    offset = 0
    try:
        while True:
            params = {
                "limit": limit,
                "offset": offset,
            }
            response = requests.get(endpoint, params=params)
            response.raise_for_status()
            data = response.json()
            
            if not data:
                logging.info("No more markets to fetch. Exiting loop.")
                break 

            all_markets.extend(data)
            logging.info(f"Fetched {len(data)} markets (offset: {offset}).")
            offset += limit
        
        return all_markets
#pagination end    
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while fetching markets: {e}")
        return []


all_markets = fetch_all_markets()

# unique check
if all_markets:
    df = pd.DataFrame(all_markets)
    unique_df = df.drop_duplicates(subset=['id']) 
# handle unusual line terminators popup
    def clean_text(value):
        if isinstance(value, str):
            return value.replace('\u2028', '').replace('\u2029', '').strip()
        return value

    unique_df = unique_df.map(clean_text)

    unique_count = len(unique_df)
    total_count = len(df)
    
    logging.info(f"Removed {total_count - unique_count} duplicate markets.")
    
    csv_path = 'cache/all_markets.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8') as file:
        unique_df.to_csv(file, index=False)
    logging.info(f"Unique markets saved to '{csv_path}' ({unique_count} total).")
else:
    logging.info("No markets found.")



#first day 22796
#second day 22830
#third day 23028