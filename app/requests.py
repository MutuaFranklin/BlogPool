import urllib.request,json
from .models import Quote



quote_url = None


# Getting api key an source links
def configure_request(app):
    global quote_url
    quote_url = app.config['QUOTE_API_URL']

def get_quote():
    '''
    Function that gets the json response to our url request
    '''
    # get_quote_url = quote_url
    # with urllib.request.urlopen(get_quote_url) as url:
    #     get_quote_data = url.read()
    #     get_quote_response = json.loads(get_quote_data)

    #     quote_results = None

    #     if get_quote_response:
    #         quote_results_list = get_quote_response
    #         quote_results = process_results(quote_results_list)


    # return quote_results


def process_results(quote_list):
    '''
    '''
    quote_results = []
    for quote_item in quote_list:
    
        author = quote_item.get('author')
        quote = quote_item.get('quote')

        
        quote_object = Quote(author, quote)
        quote_results.append(quote_object)
            

    return quote_results

