import requests

# Define the base URL of the MPV control API
base_url = 'http://127.0.0.1:5000'

# Define the URLs for different actions
play_url = base_url + '/media/play'
stop_url = base_url + '/media/stop'
volume_url = base_url + '/media/volume'

# Test play action
video_url = 'https://fallbackstream.rdi-cast.uz/listen/bar/promo'
play_data = {'url': video_url}
response = requests.post(play_url, json=play_data)
print("Play Response:", response.json())

input("Press enter to change volume")

# Test volume change action
def change_volume(volume_level):
    volume_data = {'volume': volume_level}
    response = requests.post(volume_url, json=volume_data)
    return response

volume_level = 50  # Set desired volume level here
response = change_volume(volume_level)
print("Volume Change Response:", response.json())

input("Press enter to stop")

# Test stop action
response = requests.post(stop_url)
print("Stop Response:", response.json())
