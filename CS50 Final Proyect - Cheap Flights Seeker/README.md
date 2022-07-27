# CFS (CHEAP FLIGHT SEEKER)
#### Video Demo:  https://youtu.be/V3wzfH5ZBuY
#### Description: 

Hello! 
Have you ever had the feeling that you paid for an expensive airline ticket or wondered why ticket prices vary so much? 
Maybe, like me, you've asked yourself the question: how much do agencies really pay for that flight you're buying? 

**A little personal history of the project)

Doing this course one day I was talking to my uncle and he was complaining about the high prices he was seeing on flights. 
Obviously with the current situation of oil at such high prices I thought his complaint was reasonable. 
Finally at one point in the conversation he said to me, "If you hear of any cheap flights let me know".
After that I got to thinking, why is it so expensive, why does the price vary so much, how much do the agencies pay for the flight? 
Is there any way to know when it is more convenient to travel? 
With so many pages and different prices, I decided to see if there was an API that would help me solve the problem....

**And now finally the project description!	

And after researching different APIs I came across the Amadeus API. One of the most important companies worldwide in the travel industry.
Now the program by specifying a range of dates, origin and destination, returns a ranking of the cheapest flights noted in the Amadeus system. 
In this way, you will be able to know the price that the chosen travel agency has access to and know approximately how much you are paying for the flight you want to buy. 

**How to interpret the output

The program automatically creates a .json file in the specified folder for each day, in order to save the local information provided by the API and thus minimize the 
queries to it. Also at the end it creates a final file that compiles all the previous ones.
The output will be printed on a web page as a list of tuples, as follows: (0, '1', 727.59, '2022-11-01'). 
The first number is the number of the .json file created in the folder and the second is the "id" of the offer within that file. 
The third number is the price of the flight in euros and the last one is the date of the flight.
Finally the program will print as text more information about the cheapest flights with the corresponding details,
in case you are interested in some extra information.




	
