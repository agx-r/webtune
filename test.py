import requests

# Define the base URL of the MPV control API
base_url = 'http://127.0.0.1:5000'

# Define the URLs for different actions
play_url = base_url + '/play'
stop_url = base_url + '/stop'

# Test play action
video_url = 'https://fallbackstream.rdi-cast.uz/listen/bar/promo'
play_data = {'url': video_url}
response = requests.post(play_url, json=play_data)
print("Play Response:", response.json())

input("Press enter to stop")

# Test stop action
response = requests.post(stop_url)
print("Stop Response:", response.json())