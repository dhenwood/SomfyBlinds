# Somfy Blinds
This macro and python middleware code provides the means to adjust a Somfy blinds motor via a Cisco video device. A Cisco video device supports HTTP REST API calls, however the Somfy motor requires a TCP connection to be established to send commands to it. As such, a python middleware server is deployed to take the incoming REST API call to convert it to a TCP connection.

![alt text](https://www.employees.org/~dhenwood/Images/somfyDiagram.png)

An example of the REST API call from the device to the Python server is as follows. This is performed in [the macro](https://github.com/dhenwood/SomfyBlinds/blob/main/somfyMacro.js).
```http
POST {pythonServer}/motor
Content-Type: application/json

{
  "motorIpAddress": "{motorIpAddress}",
  "pin": "{motorPin}",
  "percent": 50
}
```

