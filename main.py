import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_FUNCTION = "TIME_SERIES_DAILY"
STOCK_API_KEY = "***********"

NEWS_API_KEY = "***********"

TWILIO_SID = "***********"
TWILIO_AUTH_TOKEN = "***********"

parameters = {
    "function": STOCK_FUNCTION,
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, params=parameters)
data = response.json()["Time Series (Daily)"]

data_arr = [value for (key, value) in data.items()]
last_day_data = data_arr[0]
last_day_closing_price = last_day_data["4. close"]

print(last_day_closing_price)

before_last_day_data = data_arr[1]
before_last_day_closing_price = before_last_day_data["4. close"]
print(before_last_day_closing_price)

difference = abs(float(last_day_closing_price) - float(before_last_day_closing_price))
print(difference)

diff_percent = (difference / float(last_day_closing_price)) * 100
print(diff_percent)

if diff_percent >= 5:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }

    news_response = requests.get(NEWS_ENDPOINT, params=news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"Headline: {article['title']}. \nBrief: {article['description']}" for article in
                          three_articles]

    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(body=article, from_="+12183079637", to="+905432752775")