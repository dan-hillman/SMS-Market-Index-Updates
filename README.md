# SMS Market Index Updates

> This was my first programming "project" that was actually used in a real business. With that said, it's pretty rough and spaghetti-ish. Thanks for understanding.

## What is it?
SMS Market Index Updates is a Python script that sends an SMS (text) message containing market index updates using the Twilio API. If you would like to use this script, start a trial with Twilio at [https://www.twilio.com/try-twilio](https://www.twilio.com/try-twilio).

## Why did I make it?
I developed it while working as an intern at a financial portfolio management company. My boss was heading out of town for nearly a month and wanted a way to access market index data in the situation that cell data was slow or hard to get. They asked me to send an hourly text to their phone containing updates on daily changes in the S&P 500, NASDAQ, Dow Jones Industrial, etc.

It soon became apparent that typing out these updates proved inefficient and tedious. Not to mention, the markets sometimes would change moderately from the time I'd start typing to when I'd send the text. So, with my limited Python knowledge about web scraping, I hammered out this script and ran it on a DigitalOcean droplet. It worked, and my boss was happy.

## How does it work?
This script checks each hour if the New York Stock Exchange is open by checking a page on the Fidelity website. If the New York Stock Exchange is open, it begins to download HTML files from the Wall Street Journal's website. Specifically, it downloads the pages that contain data about each major global market index. Using regular expressions, it finds the relevant data in the HTML files. When the data has been found, it is then formatted into a string. This string is then sent through the Twilio API to the phone number that would be supplied in the code by the developer.

## Usage
Supply the proper Twilio credentials in the code. Execute the script on a PC or server. The script will send texts every hour while the New York Stock Exchange is open.

<div class='tableauPlaceholder' id='viz1495681765637' style='position: relative'><noscript><a href='#'><img alt='Borrower APR, Stated Monthly Income, and Credit Score by Occupation ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pr&#47;ProsperLoansBorrowerAPRStatedMonthlyIncomeandCreditScorebyOccupation&#47;Sheet1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='site_root' value='' /><param name='name' value='ProsperLoansBorrowerAPRStatedMonthlyIncomeandCreditScorebyOccupation&#47;Sheet1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Pr&#47;ProsperLoansBorrowerAPRStatedMonthlyIncomeandCreditScorebyOccupation&#47;Sheet1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1495681765637');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>
