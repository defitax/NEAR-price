from datetime import datetime
import requests
from time import sleep

def get_historical_price(coin_id, timestamp, currency='usd', retries=5, backoff_factor=0.5):
   # Convert the timestamp to a date
   date = datetime.utcfromtimestamp(timestamp).strftime('%d-%m-%Y')
   
   url = f'https://api.coingecko.com/api/v3/coins/{coin_id}/history'
   params = {'date': date, 'localization': 'false'}
   for attempt in range(retries):
       try:
           response = requests.get(url, params=params)
           response.raise_for_status() # Raise an HTTPError if the HTTP request returned an unsuccessful status code
           data = response.json()
           price = data.get('market_data', {}).get('current_price', {}).get(currency)
           return price
       except requests.exceptions.HTTPError as e:
           print(f"HTTP error occurred: {e}")
           sleep((2 ** attempt) * backoff_factor)
       except requests.exceptions.ConnectionError as e:
           print(f"Connection error occurred: {e}")
           sleep((2 ** attempt) * backoff_factor)
       except requests.exceptions.RequestException as e:
           print(f"Error occurred: {e}")
           sleep((2 ** attempt) * backoff_factor)
   return None

# Get user inputs
timestamp = int(input("Enter a timestamp: "))
coin_id = input("Enter a coin id: ")
currency = input("Enter a currency: ")

price = get_historical_price(coin_id, timestamp, currency)
if price:
   print(f"The historical price of {coin_id} on {timestamp} was {price} {currency}")
else:
   print("Failed to retrieve the historical price after several retries.")
