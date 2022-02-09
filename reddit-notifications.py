#Rini94
#Send notification on Telegram channel when the new reddit posts in any subreddit matches the keywords
import time
import requests
import json

config_file = open('/reddit-notifications-config.json')
config_data = json.load(config_file)
any_keywords = config_data["any_keywords"]
definite_keywords = config_data["definite_keywords"]
run = config_data["run"]
subreddit = config_data["subreddit"]
last_fetch_time = int(str(config_data["last_fetch_time"]))
bot_token = config_data["bot_token"]
channel_id = config_data["channel_id"]


def send_message (message):
	url = "https://api.telegram.org/bot" + bot_token + "/sendMessage?chat_id=" + channel_id + "&text=" + message
	requests.get (url)


def send_notification (title, link):
	if title == "failed":
		send_message ("Fetching data from webpage failed...")
	else:
		send_message ("Keywords found.\n\nPost title: " + title + "\n\nPost link: " + link)

def update_config ():
	last_fetch_time = str(int(time.time()))
	config_data["last_fetch_time"] = last_fetch_time
	config_json = json.dumps(config_data, indent = 4)
	with open("reddit-notifications-config.json", "w") as outfile:
		outfile.write(config_json)


url = "https://www.reddit.com/r/" + subreddit + "/new.json"
if (run == "false") or (len (any_keywords) == 0 and len (definite_keywords) == 0):
	exit ()


page = requests.get (url, headers = {'User-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36'})

if page.status_code == 200:
	page_json = json.loads (page.content)
	data = page_json["data"]
	post_list = data["children"]

	for post_json in post_list:
		post_data = post_json["data"]
		created_time = int(float(post_data.get("created_utc")))
		if (created_time < last_fetch_time):
			break
		post_title = post_data["title"].lower()

		if any (anykey in post_title for anykey in any_keywords) and all (defkey in post_title for defkey in definite_keywords):
			post_link = post_data["url"]
			send_notification (post_title, post_link)

	update_config ()
	exit ()
else:
	send_notification ("failed", None)
