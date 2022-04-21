import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))
    try:
        # Call get method of requests library with URL and parameters
        response = requests.get(url, headers={'Content-Type': 'application/json'},
                                    params=kwargs)
    except:
        # If any error occurs
        print("Network exception occurred")
    status_code = response.status_code
    print("With status {} ".format(status_code))
    json_data = json.loads(response.text)
    return json_data
# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))


# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    json_obj = json_payload["review"]
    try:
        response = requests.post(url, json=json_obj, params=kwargs)
    except:
        print("Something went wrong")
    return response

# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["docs"]
        #dealers = json.loads(json_result)
        # For each dealer object
        for dealer_doc in dealers:
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)
    print(results)
    return results

# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
def get_dealer_reviews_from_cf(url, dealerId):
    results = []
    json_result = get_request(url,dealerId=dealerId)
    if json_result:
        body = json_result["body"]
        data = body["data"]

        reviews=data["docs"]
        for review in reviews:
            review_obj = DealerReview(name = review["name"],
                dealership = review["dealership"], review = review["review"], purchase=review["purchase"],
                purchase_date = review["purchase_date"], car_make = review['car_make'],
                car_model = review['car_model'], car_year= review['car_year'], sentiment= "none")


            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            print(review_obj.sentiment)

            results.append(review_obj)
            print(results)
    return results

# Create an `analyze_review_sentiments` method to call Watson NLU and analyze text
# def analyze_review_sentiments(text):
# - Call get_request() with specified arguments
# - Get the returned sentiment label such as Positive or Negative
def analyze_review_sentiments(text):
    api_key = "4cpUHUT8-dIwhTAYl06dT1vLmXNHwpvlXAXpGdV6qG6R"
    #url="https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b77f090f-4a6c-4c07-9587-d7dbf26d7602"
    url = "https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/b77f090f-4a6c-4c07-9587-d7dbf26d7602"
    version = '2022-04-07'
    authenticator = IAMAuthenticator(api_key)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )
    natural_language_understanding.set_service_url(url)
    response = natural_language_understanding.analyze(
        text=text,
        features=Features(sentiment=SentimentOptions()),
        language="en"
    ).get_result()
    sentiment_score = str(response["sentiment"]["document"]["score"])
    sentiment_label = response["sentiment"]["document"]["label"]
    sentimentresult = sentiment_label

    return sentimentresult
