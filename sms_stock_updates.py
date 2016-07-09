import urllib2
import re
import time
from twilio.rest import TwilioRestClient
import datetime

"""All information is scraped from the Wall Street Journal website, so the
tickers must be formatted in the same way they are found on the WSJ website.
Specifically, the tickers must appear in the same way they do in the WSJ
URL. To test whether or not the US markets are open, the "is_market_open"
function will make a call to Marketwatch Dow Jones Industrial Average quote
page."""

brute_force_index_urls = ["http://quotes.wsj.com/index/DJIA",
                          "http://quotes.wsj.com/index/SPX",
                          "http://quotes.wsj.com/index/COMP",
                          "http://quotes.wsj.com/index/DX/DAX",
                          "http://quotes.wsj.com/index/UK/UKX",
                          "http://quotes.wsj.com/index/JP/NIK",
                          "http://quotes.wsj.com/index/CN/SHCOMP"]

stats_wanted = ["name","price","change","change_pct", "updated"]

stat_html_dictionary = {"name":'<span class="companyName">(.+?)</span>',
                        "symbol":'<span class="tickerName">(.+?)</span>',
                        "price":'<span id="quote_val">(.+?)</span>',
                        "change":'<span class="cr_num diff_price" id="quote_change">(.+?)</span>',
                        "change_pct":'<span class="cr_num diff_percent" id="quote_changePer">(.+?)</span>',
                        "updated":'<span class="timestamp_value" id="quote_dateTime">(.+?)</span>'
                        }

def connected(address):
    try:
        data = urllib2.urlopen(address)
        return True
    except:
        return False

def is_market_open():
    marketwatch_url = "http://www.marketwatch.com/investing/index/djia"
    while connected(marketwatch_url) == False:
        print "Lost connection trying to see if US markets are open, hold tight."
        time.sleep(5)
    market_closed_xml = '<p class="column marketstate">(.+?)</p>'
    html_file = urllib2.urlopen(marketwatch_url)
    html_text = html_file.read()
    regex = market_closed_xml
    pattern = re.compile(regex)
    found_item = re.findall(pattern, html_text)
    if found_item[0] == "Market closed":
        return False
    else:
        return True

def make_brute_force_stock_report(url_list, stats_wanted, stat_html_dictionary):
    text = str(datetime.datetime.now())+ "\n" + "\n"
    for url in url_list:
        while connected(url) == False:
            print "Lost connection while fetching WSJ data. Trying again in 5 seconds..."
            time.sleep(5)
        html_file = urllib2.urlopen(url)
        html_text = html_file.read()
        for stat in stats_wanted:
            regex = stat_html_dictionary[stat]
            pattern = re.compile(regex)
            found_stat = re.findall(pattern, html_text)
            if stat == "name":
                if found_stat[0] == "Dow Jones Industrial Average":
                    text += "**US Indexes**" + "\n" + "\n" + "Dow Jones Industrial Average" + "\n"
                elif found_stat[0] == "S&amp;P 500 Index":
                    text += "S&P 500 Index" + "\n"
                elif found_stat[0] == "DAX":
                    text += "**European Indexes**" + "\n" + "\n" + "DAX" + "\n"
                elif found_stat[0] == "NIKKEI 225 Index":
                    text += "**Asian Indexes**" + "\n" + "\n" + "NIKKEI 225 Index" + "\n"
                else:
                    text += found_stat[0] + "\n"
            elif stat == "symbol":
                text += "Symbol: " + found_stat[0] + "\n"
            elif stat == "price":
                text += "Price: " + found_stat[0] + "\n"
            elif stat == "change":
                text += "Change: " + found_stat[0] + "\n"
            elif stat == "change_pct":
                text += "%Change: " + found_stat[0] + "\n"
            elif stat == "updated":
                text += "Updated: " + found_stat[0] + "\n"
        text += "\n"
    return text

def send_text(formatted_text):
    account_sid = "" # Your Account SID from www.twilio.com/console
    auth_token  = ""  # Your Auth Token from www.twilio.com/console

    client = TwilioRestClient(account_sid, auth_token)

    message = client.messages.create(body = formatted_text,
        to = "",    # Replace with your phone number
        from_ = "") # Replace with your Twilio number

    print(message.sid)

def update_at_regular_intervals(interval_in_seconds):
    while True:
        current_time = datetime.datetime.now()
        if is_market_open() == True:
            data = make_brute_force_stock_report(brute_force_index_urls, stats_wanted, stat_html_dictionary)
            print str(current_time) + "\n"
            print data
            send_text(data)
        else:
            print "US Markets are closed. The current time is %s" % (current_time)
        time.sleep(interval_in_seconds)


update_at_regular_intervals(3600)
