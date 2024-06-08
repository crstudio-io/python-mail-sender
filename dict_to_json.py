# to convert code to json payload for testing
import json

with open("example_body.html") as body:
    body_str = body.readlines()
    print(json.dumps({
        "subject": "Login Request",
        "body": body_str,
        "to": ["aquashdw@gmail.com"],
    }))
