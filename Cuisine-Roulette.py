# TODO: write some Python code here to produce the desired output

import random
import os
from dotenv import load_dotenv
#from dotenv.main import DotEnv
from datetime import datetime
import smtplib
import ssl
import json
from pprint import pprint

#from _future_ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib


# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode

    # Yelp Fusion no longer uses OAuth as of December 7, 2017.
# You no longer need to provide Client ID to fetch Data
# It now uses private keys to authenticate requests (API Key)
# You can find it on
# https://www.yelp.com/developers/v3/manage_app


load_dotenv() # get env files from .env file

USER_NAME = os.getenv("USER_NAME")
API_KEY = os.getenv("API_KEY")
print('------------------------------------------')
print()
print("Hello " + USER_NAME + ", welcome to Cuisine Roulette!")
print("We'll find you a restaurant based on your desired cuisine and location!")
print()
print('------------------------------------------')
print()


# API constants, you shouldn't have to change these.
HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

Address = input("Please input your address: ")
print()
Price = input("Please input price limits ($-$$$$):")

print('------------------------------------------')
print()

price_num = str(len(Price))
print()
print('Is everyone in your party ready to chose a cuisine?')
print()



Cuisine_Names = []
while True:
    Cuisine_Name = input("Please input a Cuisine type, or 'DONE' if your whole party has voted: ")
    if Cuisine_Name == "DONE":
        break
    else:
        Cuisine_Names.append(Cuisine_Name)



random_choice = random.choice(Cuisine_Names)

Cuisine_Name = random_choice

print('------------------------------------------')
print()
print('Cuisine Selected: ' + Cuisine_Name)
print()
print('------------------------------------------')

SEARCH_LIMIT = 3
sort_by = 'rating'


def request(HOST, SEARCH_PATH, API_KEY, url_params=None):
    """Given your API_KEY, send a GET request to the API.
    Args:
        host (str): The domain host of the API.
        path (str): The path of the API after the domain.
        API_KEY (str): Your API Key.
        url_params (dict): An optional set of query parameters in the request.
    Returns:
        dict: The JSON response from the request.
    Raises:
        HTTPError: An error occurs from the HTTP request.
    """
    url_params = url_params or {}
    url = '{0}{1}'.format(HOST, quote(SEARCH_PATH.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(API_KEY, Cuisine_Name, Address, price_num, sort_by):
    """Query the Search API by a search term and location.
    Args:
        term (str): The search term passed to the API.
        location (str): The search location passed to the API.
    Returns:
        dict: The JSON response from the request.
    """

    url_params = {
        'term': Cuisine_Name.replace(' ', '+'),
        'location': Address.replace(' ', '+'),
        'price': price_num.replace(' ', '+'),
        'sort by': sort_by,
        'limit': SEARCH_LIMIT

    }
    return request(HOST, SEARCH_PATH, API_KEY, url_params=url_params)



def get_business(API_KEY, business_id):
    """Query the Business API by a business ID.
    Args:
        business_id (str): The ID of the business to query.
    Returns:
        dict: The JSON response from the request.
    """
    business_path = BUSINESS_PATH + business_id

    return request(HOST, business_path, API_KEY)





def query_api(Cuisine_Name, Address, price_num, sort_by):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, Cuisine_Name, Address, price_num, sort_by)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(Cuisine_Name, Address, price_num, sort_by))
        return

    business_id = businesses[0]['id']

    response = get_business(API_KEY, business_id)

    print()
    print('------------------------------------------')
    print()

    print('Restaurant Choice 1:  ...')
    pprint.pprint(response, indent=2)
    #.format(business_id)
    Restaurant_Data = response['alias']
    return Restaurant_Data
    
    business_id2 = businesses[1]['id']

    print()
    print()

    response = get_business(API_KEY, business_id2)

    print()
    print('------------------------------------------')
    print()

    print('Restaurant Choice 2:  ...'.format(business_id2))
    pprint.pprint(response, indent=2)

    business_id3 = businesses[2]['id']

    print()
    print()

    response = get_business(API_KEY, business_id3)

    print()
    print('------------------------------------------')
    print()

    print('Restaurant Choice 3:  ...'.format(business_id3))
    pprint.pprint(response, indent=2)

    print()
    print('------------------------------------------')
    print()
    
    restaurant_choice = get_business(API_KEY, business_id3)
    

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=Cuisine_Name,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=Address, type=str,
                        help='Search location (default: %(default)s)')
    parser.add_argument('-p', '--price', dest='price',
                        default=price_num, type=str,
                        help='Search price (default: %(default)s)')
    parser.add_argument('-s', '--sort_by', dest='sort_by',
                        default=sort_by, type=str,
                        help='Search sort_by (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        Restaurant_Data = query_api(input_values.term, input_values.location, input_values.price, input_values.sort_by)
        #Gathering information to send an email receipt
        while True:
            user_email_request = input("Do you want a response via email? [y/n]: ")
            if user_email_request == 'y':
                user_email = input("Please enter your email address: ")
                #Setting up sending an email
                port = 465  # For SSL
                smtp_server = "smtp.gmail.com"
                sender_email = "superdupermarketnyu@gmail.com"  
                password = input("Type the email password and press enter: ")
                message = """\
                Subject: Your response from Cuisine Roulette:


        """+Restaurant_Data

        #"Restaurant Choice: "+ Restaurant_Name +"\n"+""+"\n SUBTOTAL: "+to_usd(Subtotal)+ "\n TAX: "+to_usd(Tax)+"\n TOTAL: "+to_usd(Total)

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, user_email, message)
                break
            if user_email_request == 'n':
                print("Thanks for using Cuisine Roulette!")
                break
            if user_email_request not in ('y','n'):
                print("Please input a valid response. Try Again")

#Password: vyc^Ed*el0E6
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )


if __name__ == '__main__':
    main()








