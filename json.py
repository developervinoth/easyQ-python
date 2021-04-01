
import requests 

# Making a get request 
url='https://hqueue-node.herokuapp.com/api/getBookings'

payload={'date': "24-2-2021"}
response = requests.post(url,data = payload) 

# print response 
print(response) 

# print json content 
bookings = response.json() 

bookings = bookings["data"]["bookings"]
id = "15-30"
for booking in bookings:
    if(booking["Id"] == id):
        print("true")
    updated = booking
    updated["patientVisited"] = True
    url='https://hqueue-node.herokuapp.com/api/userVisited'
    payload = updated
    response = requests.post(url,data = payload) 
    print(response.json())

