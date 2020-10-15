# LearnForFree
LearnForFree is a search engine to find free educational content for every topic a person would need.
It searches and indexes many different sites to give the best results tailored to the search.
You can search any topic and get the best results back!

No excuses; start learning today!

## Technical context
We wanted to create an app that fetches results from multiple sources. There were a total of 7 different platforms
for free courses that we will be making use of, and by the time of the deadline we successfully wrapped 2 (almost 3!)
of them. We are currently using, and will be using any techniques in order to get the data, including API calls,
pre-saving an index into a file, scraping, and even Selenium!

## List of providers with status
Provider name | Status | Message
------- | ---- | -------------
edX | :white_check_mark: | currently implemented via one-time fetching of the index into a file, and using it for the search. The edX also has an API but there's no uri for keyword search, making it extremely lengthy to do it this way.
Futurelearn | :white_check_mark: | successfully implemented via web scraping
Coursera | :large_blue_diamond: | To be implemented via Selenium (pagination is dynamic)
khan academy | :large_blue_diamond: | To be researched (it doesnt have courses, but other materials such as articles, so we'll decide on how to incorporate that)
openwho dot org | :large_blue_diamond: | To be implemented via Selenium (object population and pagination are dynamic)
alison | :large_blue_diamond: | To be researched