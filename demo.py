from __future__ import absolute_import

from six.moves import range

from automation import CommandSequence, TaskManager

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = [#'https://www.reddit.com',
         #'https://www.nytimes.com',
         #'http://www.cnn.com',
         #'https://www.cricbuzz.com',
         #'http://www.nba.com',
         'http://www.accuweather.com/']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
#for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
browser_params[0]['http_instrument'] = False
    # Enable flash for all three browsers
browser_params[0]['disable_flash'] = True
browser_params[0]['headless'] = True  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)
def callGet(**kwargs):
    driver = kwargs['driver']
    js = "var output = [];"\
	  "function getCPM()"\
	  "{"\
	  "	var responses = pbjs.getBidResponses();"\
	  "	Object.keys(responses).forEach(function(adUnitCode){"\
	  "	var response = responses[adUnitCode];"\
	  "		response.bids.forEach(function(bid)"\
	  "		{"\
	  "			output.push({"\
	  "			"\
	  "			adunit: adUnitCode,"\
	  "			adId:bid.adId,"\
	  "			bidder:bid.bidder,"\
	  "			cpm: bid.cpm"\
	  "			});"\
	  "		});"\
	  "	});"\
	  "}"\
	  "getCPM();"\
	  "return output;"
    status = driver.execute_script(js)
    #print(status)
    f = open('result.txt','r+')
    f.read()
    stl = [str(i) for i in status]
    st = ' '.join(stl)
    f.write('\r\n')
    f.write(st)
    f.close()
    print(status)
    return

# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)

    # Start by visiting the page
    command_sequence.get(sleep=0, timeout=100)
    command_sequence.run_custom_function(callGet)

    # dump_profile_cookies/dump_flash_cookies closes the current tab.
    # command_sequence.dump_profile_cookies(120)

    # index='**' synchronizes visits between the three browsers
    manager.execute_command_sequence(command_sequence, index=None)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
