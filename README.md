# Somfy Blinds
This macro and python middleware code provides the means to adjust a Somfy blinds motor via a Cisco video device. A Cisco video device supports sending HTTP REST API requests, however the Somfy motor requires a TCP connection to be established to send commands to it. As such, a python middleware server is deployed to take the incoming REST API call to convert it to a TCP connection.

![alt text](https://www.employees.org/~dhenwood/Images/somfyDiagram.png)

## Setup
From a server runnings Linux, install and run the [python code](https://github.com/dhenwood/SomfyBlinds/blob/main/somfy.py). Test the python code and Somfy integration by sending the below HTTP REST request. Change the below percent value to numbers between 0 and 100 and ensure the blind adjusts.

```http
POST {pythonServer}:8000/motor
Content-Type: application/json

{
  "motorIpAddress": "{motorIpAddress}",
  "pin": "{motorPin}",
  "percent": 50
}
```

