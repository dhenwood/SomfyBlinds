from flask import Flask, request, jsonify
import requests, json, time
import urllib3

urllib3.disable_warnings(
    urllib3.exceptions.InsecureRequestWarning
)

app = Flask(__name__)

@app.route('/motor', methods=['POST'])
def rxMessage():
    data = request.get_json()
    somfyIpAddress = data.get("motorIpAddress")
    somfyPin = data.get("pin")
    percent = data.get("percent")

    changePercent(somfyIpAddress, somfyPin, percent)
    responseMsg = {"status": "ok"}
    return jsonify(responseMsg)

class SomfyMotor:

    def __init__(self, ip):
        self.ip = ip
        self.base_url = f"https://{ip}"
        self.req_url = f"{self.base_url}/req"

        self.session = requests.Session()
        self.session.verify = False

    def login(self, pin):

        print("Connecting to Somfy motor...")

        try:
            # First establish a web session
            self.session.get(
                self.base_url + "/",
                timeout=10
            )

            # Submit the PIN using form encoding
            response = self.session.post(
                self.base_url + "/",
                data={"password": pin},
                headers={
                    "Content-Type":
                        "application/x-www-form-urlencoded"
                },
                timeout=10
            )

            response.raise_for_status()

            print("Login HTTP status:", response.status_code)

            # Check whether we have a session cookie
            session_id = self.session.cookies.get("sessionId")

            if session_id:
                print("Session cookie obtained!")
                print("Login completed.")
                return True

            print("No sessionId cookie received.")
            print("Response:", response.text[:500])
            return False

        except requests.RequestException as error:
            print("Login failed:", error)
            return False

    def send_command(self, method, params=None):
        payload = {
            "method": method,
            "params": params or {},
            "id": 1
        }

        try:
            response = self.session.post(
                self.req_url,
                json=payload,
                headers={
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                timeout=10
            )

            response.raise_for_status()

            result = response.json()

            print(method, ":", result)

            return result

        except requests.RequestException as error:
            print("Command failed:", error)
            return None

    def move_to(self, position):
        if not 0 <= position <= 100:
            raise ValueError("Position must be 0-100")

        return self.send_command(
            "move.to",
            {
                "position": position,
                "priority": 0
            }
        )

    def open(self):
        return self.move_to(100)

    def close(self):
        return self.move_to(0)

    def stop(self):
        return self.send_command("move.stop")


# --------------------------------
# Main program
# --------------------------------
def changePercent(somfyIpAddress, somfyPin, percent):
    print("about to start...")
    motor = SomfyMotor(somfyIpAddress)
    pin = somfyPin

    if motor.login(pin):
        print("\nSomfy motor ready!")
        motor.move_to(percent)

        # Other examples:
        # motor.open()
        # motor.close()
        # motor.stop()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
