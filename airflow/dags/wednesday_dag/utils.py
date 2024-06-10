import requests
import json
import os


def send_to_teams(image_url, quote):
    webhook_url = os.getenv('TEAMS_WEBHOOK_URL')
    headers = {
        'Content-Type': 'application/json'
    }
    message = {
        '@type': 'MessageCard',
        '@context': 'http://schema.org/extensions',
        'summary': 'Daily Inspiration',
        'sections': [{
            'activityTitle': 'Valentin Krivolutskii:',
            'text': quote,
            'images': [{
                'image': image_url
            }]
        }]
    }
    response = requests.post(
        webhook_url,
        headers=headers,
        data=json.dumps(message)
    )
    return response.text
