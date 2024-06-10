# Functions used for Building a REST API for an Edinburgh-Based Startup: Real-Time Ticketmaster Event Notifications. #

The code allows you to scan ticketmaster, in any country you desire (identified by their ID on the API docs). It then saves events to a csv file, this is the inital stage of loading the events. Once this is run, anytime you run the fetch new events function you are returended with events that have recently been added. Scans up to 7 years in advance. Code also intelligently gets around paging restrictions from the API. 
