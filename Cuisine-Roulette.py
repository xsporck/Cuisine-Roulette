

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

print("Hello " + USER_NAME + ", welcome to Cuisine Roulette!")
print("We'll find you a restaurant based on your desired cuisine and location!")
print()

# API constants, you shouldn't have to change these.
HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.


Cuisine_Name = input("Please input a Cuisine type: ")
Address = input("Please input your address: ")
SEARCH_LIMIT = 3

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


def search(API_KEY, Cuisine_Name, Address):
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



def query_api(Cuisine_Name, Address):
    """Queries the API by the input values from the user.
    Args:
        term (str): The search term to query.
        location (str): The location of the business to query.
    """
    response = search(API_KEY, Cuisine_Name, Address)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(Cuisine_Name, Address))
        return

    business_id = businesses[0]['id']

    print(u'{0} businesses found, querying business info ' \
        'for the top result "{1}" ...'.format(
            len(businesses), business_id))
    response = get_business(API_KEY, business_id)

    print(u'Result for business "{0}" found:'.format(business_id))
    pprint.pprint(response, indent=2)
    
    business_id2 = businesses[1]['id']

    print()
    print()
    print(u'{0} businesses found, querying business info ' \
        'for the second result "{1}" ...'.format(
            len(businesses), business_id2))
    response = get_business(API_KEY, business_id2)

    print(u'Result for business "{0}" found:'.format(business_id2))
    pprint.pprint(response, indent=2)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=Cuisine_Name,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=Address, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
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

"""+"HERE IS THE RESPONSE"

#"Checkout at: "+ dt_string+"\n"+"".join(response) +"\n SUBTOTAL: "+to_usd(Subtotal)+ "\n TAX: "+to_usd(Tax)+"\n TOTAL: "+to_usd(Total)

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