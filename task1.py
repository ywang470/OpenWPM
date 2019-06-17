from __future__ import absolute_import

from six.moves import range

from automation import CommandSequence, TaskManager

from sys import platform

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = ['https://www.reddit.com',
         'https://www.nytimes.com',
         'http://www.cnn.com',
         'https://www.cricbuzz.com',
         'http://www.nba.com',
         'http://www.accuweather.com/']

# Loads the manager preference and 3 copies of the default browser dictionaries
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
#for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
browser_params[0]['http_instrument'] = True
    # Enable flash for all three browsers
browser_params[0]['disable_flash'] = False
if platform != 'darwin':
    browser_params[0]['headless'] = True  # Launch only browser 0 headless

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params['data_directory'] = '~/Desktop/'
manager_params['log_directory'] = '~/Desktop/'

# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)



# Visits the sites with all browsers simultaneously
for site in sites:
    command_sequence = CommandSequence.CommandSequence(sites)

    # Start by visiting the page
    command_sequence.get(sleep=0, timeout=60)

    # index='**' synchronizes visits between the three browsers
    manager.execute_command_sequence(command_sequence, index='**')

# Shuts down the browsers and waits for the data to finish logging
manager.close()
