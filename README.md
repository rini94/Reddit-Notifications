# Reddit-Notifications

The script can be run in the background using Linux crontab or online using services like Heroku. It checks the website on scheduled time for needed content and sends notification on Telegram.

`reddit-notifications-config.json` contains the configurations needed to run the script.

To edit crontab use

```
crontab -e
```

add the line to execute the script every 10 minutes from tuesday to thursday.

```
*/10 * * * 2-4 python <location>/reddit-notifications.py
```
