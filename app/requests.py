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

    with urllib.request.urlopen(quote_url) as url:
        get_quote_data = url.read()
        quote_response = json.loads(get_quote_data)


        if quote_response:
            author = quote_response.get('author')
            quote = quote_response.get('quote')
            new_quote =Quote(author, quote)
            return new_quote

        else:
            author = 'Destiny can be delayed but can never be denied'
            quote = 'Unknown'
            new_quote =Quote(author, quote)
            return new_quote





