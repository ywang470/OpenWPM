from __future__ import absolute_import

from six.moves import range

from automation import CommandSequence, TaskManager
from selenium import webdriver


NUM_BROWSERS = 1
sites = ['http://www.accuweather.com/']

manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
      browser_params[0]['http_instrument'] = True
    # Enable flash for all three browsers
    # browser_params[i]['disable_flash'] = False
      browser_params[0]['headless'] = True  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'


manager = TaskManager.TaskManager(manager_params, browser_params)
def callGet(**kwargs):
    driver = kwargs['driver']
    js ='return pbjs.getBidResponses()[Object.keys(pbjs.getBidResponses())[0]].bids[0].bidder'
    js1 ='return pbjs.getBidResponses()[Object.keys(pbjs.getBidResponses())[0]].bids[0].adId'
    js2 ='return pbjs.getBidResponses()[Object.keys(pbjs.getBidResponses())[0]].bids[0].cpm'
    js3 = "var output = [];"\
	  "function getCPM()"\
	  "{"\
	  "	var responses = pbjs.getBidResponses();"\
	  "	Object.keys(responses).forEach(function(adUnitCode){"\
	  "	var response = responses[adUnitCode];"\
	  "		response.bids.forEach(function(bid)"\
	  "		{"\
	  "			output.push({"\
	  "			bid:bid,"\
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
    js4 = 'return Object.keys(pbjs.getBidResponses())[0]'
    #bidder = driver.execute_script(js)
    #ID = driver.execute_script(js1)
    status = driver.execute_script(js4)
    #print(bidder)
    #print(ID)
    print(status)
    return 

 
for site in sites:
    command_sequence = CommandSequence.CommandSequence(site)
    command_sequence.get(sleep=10, timeout=100)
    command_sequence.run_custom_function(callGet)
    manager.execute_command_sequence(command_sequence,index='**')


manager.close()
