import xapi from 'xapi';

let pythonServer = "<pythonServer>"
let motorIpAddress = "<ipAddress>"
let motorPin = "<pin>"

var peopleInRoom = 0 // Do not change. Used in macro.

function httpPost(percent){
  let url = `${pythonServer}:8000/motor`
  let header = "Content-Type: application/json"
  let body = `{"motorIpAddress": "${motorIpAddress}", "pin": "${motorPin}", "percent": ${percent}}`
  xapi.Command.HttpClient.Post({ AllowInsecureHTTPS: "true", Header: header,  Url: url }, body);
}

// Track people presence
xapi.Status.RoomAnalytics.PeopleCount.Current.on((count) => {
  if (count > 0 && peopleInRoom == 0) {
    httpPost(0) // Open Blinds
  }else if (count == 0){
    httpPost(100)  // Close Blinds
  }
  peopleInRoom = count
})
