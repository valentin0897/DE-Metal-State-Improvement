import os
import json

import requests

IMAGE_SERVICE_URL = 'https://api.unsplash.com/photos/random'
QUOTE_SERVICE_URL = (
    'https://shakespeare1.p.rapidapi.com/shakespeare/generate/lorem-ipsum'
)


def load_random_picture():
    unsplash_access_key = os.getenv('UNSPLASH_ACCESS_KEY')
    headers = {
        'Authorization': f'Client-ID {unsplash_access_key}'
    }
    response = requests.get(
        IMAGE_SERVICE_URL,
        headers=headers
    )
    response.raise_for_status()
    image_url = response.json().get('urls').get('regular')
    return image_url


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


def get_quote():
    url = QUOTE_SERVICE_URL

    headers = {
        'X-RapidAPI-Key': os.getenv('RAPIDAPI_KEY'),
        'X-RapidAPI-Host': 'shakespeare1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers)

    print(response.json()['contents']['lorem-ipsum'])
