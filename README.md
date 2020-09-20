# Armenian petrol prices parser

This repository contains scripts for getting and parsing the petrol prices of Armenia. The task itself is not complicated, but the main goal here is to get a website, 
that will contain the history of prices, will be updated every day and won't require any money to maintain.

So the solution that I found and wanted to implement is this:
* have 2 repositories
  * parser and publisher - will be deployed into a google function, which provides some limited number of calls forever as part of free tier
  * website - https://github.com/KoStard/petrol_price_history_arm/ - will render the results
* how will we collect the information? Maybe we can use some database? But for that we will get the restrictions coming with that + permissions... So the free solution that 
I came with is to use the website repository as a database too. This can be implemented with the GitHub API, which allows us creating new files with provided content. So we 
create a folder "history", in which we will have 1 json file for every day, containing the prices. The file will be named with format "yyyy-mm-dd.json". In the front-end we 
will try to fetch data of past 31 days, so that even if the data is not available, we will just skip that data point in the graph. So after this, the only thing that we need
to do, is to run the "parser and publisher" every day, publish the prices into the website repository as json files, which will be used by the front-end, which can be 
accessed with the GitHub Pages.
The final result - https://kostard.github.io/petrol_price_history_arm/

Limitations:
* Google functions - 2 million calls per month, which is very high, considering our usages
* GitHub pages
  * the project using github pages can't be bigger than 1 GB. The limit for regular projects is 100GB, which means that in theory we can move the old data into 
another project to bypass this limitation
  * bandwidth limit of 100GB per month, which should be quite high for us, as we are loading only 31 days data, 
which will be around 31 * 0.5KB = 15KB and +5KB for other files loaded from the repository, we get ~20KB, which can grow if we add some other providers, so let's consider we 
add 4 more providers and the code grows 5 times, we may get 100KB for each page load, which will result to ~1 million page loads per month and if the regular user opens the 
website 2 times per day, we can have around 17K active users. 
* The number of loaded days - considering the architecture of the database, we are loading every day's prices separately, which means that the duration of loading everything
will increase proportionally and because it includes network in the chain, it may take some time. So I am currently using 31 days, to get the last month's data and if the user 
needs more information, then they can download the project and get whole available history. Also, increasing the number of loaded days, we may get to the github pages limit 
faster, if the number of users grows.
