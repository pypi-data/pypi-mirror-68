"""
jobs.py

Show a simple example of how to define a custom job and pass it to the ZdmClient.

"""
import json
import time

from zdm import ZDMClient

device_id = '*** PUT YOU DEVICE ID HERE ***'
password = '*** PUT YOUR PASSWORD HERE ***'

device_id = "dev-4wv0e6felpuc"

password = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHd2MGU2ZmVscHVjIiwidXNlciI6ImRldi00d3YwZTZmZWxwdWMiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.rHZYv1mP6TJuBHLOjlzSiVoYHKqpLZ9iguCzj2hw6TM"

device_id = "dev-4wvkhcqc0fip"
password = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkZXYtNHd2a2hjcWMwZmlwIiwidXNlciI6ImRldi00d3ZraGNxYzBmaXAiLCJrZXkiOjEsImV4cCI6MjUxNjIzOTAyMn0.Q8B9NFT5fFdJ1NCne3y8uxbfXNFH9gSfLCIvPJtKM1c"

def set_temp(zdmclient, args):
    # zdmclient: is the object of the ZdmClient.
    # args     : is a json with the arguments  of the function.
    print("Executing job set_temp. Received args: {}".format(args))
    # DO SOMETHING
    # return: a json with the result of the job.
    return json.dumps({"msg": "Temperature set correctly."})


# A dictionary of jobs where the key is the name of the job and value if the callback to execute.
my_jobs = {
    "dad": set_temp,
}

device = ZDMClient(device_id=device_id, jobs=my_jobs)
device.set_password(password)
device.connect()

while True:
    time.sleep(3)
