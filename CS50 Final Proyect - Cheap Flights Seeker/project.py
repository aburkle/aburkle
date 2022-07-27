

# CFS (CHEAP FLIGHT SEEKER)
# This program  helps you to find the cheapest flight in a determined period of time from the Amadeus system.

import streamlit as st
from amadeus import Client
import json
from datetime import timedelta, datetime
import ama_keys


def main():
    
    amadeus = Client(
        client_id=ama_keys.client_id,
        client_secret=ama_keys.client_secret
    ) 
    while True:
        
        try:
            
            start_date= input('Insert a starting date: (YYYY-MM-DD) ')
            end_date =  input('Insert a finishing date: (YYYY-MM-DD) ')
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            print ("Incorrect data format, should be YYYY-MM-DD")
            pass
    
        origin = input('Insert a starting airport (IATACode), if you need help you can search in this website: https://www.world-airport-codes.com/: ').upper()
        destiny = input('Enter the destination airport (IATACode): ').upper()
        destiny_path = input('Insert the destination folder path: ')
        
        if len(origin) != 3 or len(destiny) != 3:
            print("The IATACode has 3 letters")
            pass
        elif len(origin) == 3 or len(destiny) == 3:
            break
        else:
            pass
        
    json_creator(amadeus,start_date,end_date,origin, destiny, destiny_path)
    data = json_consolidator(start_date,end_date,destiny_path)
    
    elem, details = cheap_price_getter(data,start_date)
    
    st.title('RESULTS OF THE QUERY CFS (CHEAP FLIGHT SEEKER)')
    st.write()
    st.write(f"Top 20 cheapest flights in the period {start_date} - {end_date}: ",elem[:20])
    st.write('Explanation of the output: ')
    st.write()
    st.write('The 1st number is the number of the .json file created in the folder and the 2nd is the "id" of the offer inside that file.')
	
    st.write('The 3rd number is the price of the flight in Euros and the last one is the date of the flight.')
    st.write()
    st.title('DETAILS OF THE TOP 5  CHEAPEST FLIGHTS')
    st.write()
    
    for i,detail in enumerate(details):
        ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])
        if i == 0:
            st.write(f"The price of the cheapest flight is: {details[i]['price']['grandTotal']} {details[i]['price']['currency']}")
            st.write()
        else:
            st.write(f"The price of the {ordinal(i+1)}-cheapest  flight is: {details[i]['price']['grandTotal']} {details[i]['price']['currency']}")
            st.write()
        
        segments =  details[i]['itineraries'][0]['segments']
        for x in range(len(segments)):
            try:
                st.write(f"The flight {segments[x]['carrierCode']}{segments[x]['number']} departs from {segments[x]['departure']['iataCode']}, the {segments[x]['departure']['at']} and arrives at {segments[x]['arrival']['iataCode']} the {segments[x]['arrival']['at']}")
                st.write()
            except KeyError:
                pass
        
        if i == 0:
            st.write(f"Details of the cheapest flight: ")
            st.write()
        else:
            st.write(f"Details of the {ordinal(i+1)}-cheapest flight: ")
            st.write()
        
        
        st.json(detail)
        st.write()


def json_creator(amadeus,start_date,end_date, origin, destiny, destiny_path):
    
    for n in range(int((end_date - start_date).days)):

        departure_date = start_date + timedelta(n)

        response = amadeus.shopping.flight_offers_search.get(
            originLocationCode=origin,
            destinationLocationCode=destiny,
            departureDate=departure_date,
            adults=1)
        json_file = response.data
        with open("{}".format(destiny_path) + "/ama_response_{}.json".format(n), 'w') as fp:
        
            json.dump(json_file,fp) 
    
    return True
    

def json_consolidator(start_date, end_date, destiny_path):
    
    data = [] # This list stores the whole data, the compilation of all the json files.

    with open ("{}".format(destiny_path) +"/ama_response_final.json", "w", encoding='utf-8') as file:
        for n in range(int((end_date - start_date).days)):
            with open ("{}".format(destiny_path) + "/ama_response_{}.json".format(n),"r",encoding='utf-8') as fp:
                data.append(json.load(fp))
    return data

def cheap_price_getter(data,start_date):

    
    z = [] # This list will store all the prices
    x = [] # This list will store all the id's
    w = [] # This list will store all the days of the period
    u = [] # This list will store the days as dates
    elem = [] # This list stores only the z,x,w elements (day, id, price) ordered from the cheapest to the most expensive. 
    details = [] # This list will store all the available data retrieved by the API from the cheapest flights.

    


    for i in range(len(data)): #this loops through days
        for y in range(len(data[i])): # this loops through ids of the day
            z.append(float(data[i][y]['price']['grandTotal'])) # This is going to be the price
            x.append(data[i][y]['id']) # This is going to be the Id as string 
            w.append(i) # this is going to be the day
            u.append((start_date + timedelta(i)).strftime("%Y-%m-%d"))


    y = list(zip(w,x,z,u)) # This is the list of tuples with all the elements mentioned above       
    y.sort(key=lambda x:x[2]) # This is the list ordered by price descending

    for x in y: # for every tuple of the list, if  the price is = to the price of the place before of the list, just ignore it, 
        # if it is different, add it into the list.
        
        if x == y[0]:
            elem.append(x)
        elif x[2] == y[(y.index(x)-1)][2]: #This line just skip if 2 consecutive elements have the same price. That is necessary 
            pass
        else:
            elem.append(x) # elem is the just the 'y' list without duplicates.

    elem.sort(key=lambda x:x[2])

    for i in range(5):
        details.append(data[elem[i][0]][(int(elem[i][1])-1)]) # takes the first tuple of the list 'elem' 
        # and returns the first element of that tuple which is the day as integer, which is the position of the element in the list 
        # corresponding to that day. And inside that day I looks for the 'id' passed in the 2nd part. 

    return elem, details

if __name__=="__main__":
    main()


