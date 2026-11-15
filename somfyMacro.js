import xapi from 'xapi';

let motorIpAddress = "<ipAddress>"
let motorPin = "<pin>"

function httpPost(percent){
  let url = "<pythonServer>/motor"
  let header = "Content-Type: application/json"
  let body = `{"motorIpAddress": "${motorIpAddress}", "pin": "${motorPin}", "percent": ${percent}}`
  xapi.Command.HttpClient.Post({ AllowInsecureHTTPS: "true", Header: header,  Url: url }, body);
}

// Button presses
xapi.event.on('UserInterface Extensions Widget Action', (event) => {
  if(event.WidgetId == 'blindsBtn' && event.Type == 'pressed'){
    let percent = event.Value
    httpPost(percent)
  }
})
