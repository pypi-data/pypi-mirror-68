"""
basic.py

Show the basic example of a ZdmClient that sends a stream of messages to the ZDM.
Each message is published into a random tag with a random temperature value.

"""
import random
import time
import zdm

device_id = 'device_id'
password = 'password'

device_id = "dev-4w74dufrqqkz"

password = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHc3NGR1ZnJxcWt6IiwidXNlciI6ImRldi00dzc0ZHVmcnFxa3oiLCJrZXkiOjIsImV4cCI6MjUxNjIzOTAyMn0.sefnr9JkBMP4_h9IC-2XAbek7ZHBk0CKQsC0ysN_1Y0"

device_id = "dev-4wvkhcqc0fip"
password = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHd2a2hjcWMwZmlwIiwidXNlciI6ImRldi00d3ZraGNxYzBmaXAiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.Q8B9NFT5fFdJ1NCne3y8uxbfXNFH9gSfLCIvPJtKM1c"


device_id = "dev-4vkg30lcssn7"
password ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZGV2LTR2a2czMGxjc3NuNyIsImV4cCI6MTU5MTk1MTg3MSwic3ViIjoiZGV2LTR2a2czMGxjc3NuNyIsImtleSI6MX0.QycdQgKadD8p5iTGT2PPWYEXfniQQGB0kEjhiYA4WFE"

def pub_random():
    # this function is called periodically to publish to ZDM random int value labeled with tags values
    print('------ publish random ------')
    tags = ['tag1', 'tag2', 'tag3']

    for t in tags:
        value = random.randint(0, 20)
        payload = {
            'value': value
        }
        # publish payload to ZDM
        device.publish_data(t, payload)
        print('published on tag:', t, ':', payload)

    print('pub_random done')


def pub_temp_pressure():
    # this function publish another payload with two random int values
    print('---- publish temp_pressure ----')
    tag = 'tag4'
    temp = random.randint(19, 23)
    pressure = random.randint(50, 60)
    payload = {'temp': temp, 'pressure': pressure}
    device.publish_data(tag, payload)
    print('published on tag: ', tag, ':', payload)


device = zdm.ZDMClient(device_id=device_id, endpoint="rmq.localhost")
device.set_password(password)
device.connect()

while True:
    time.sleep(2)
    pub_random()
    pub_temp_pressure()
