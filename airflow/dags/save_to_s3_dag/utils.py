import os
import json
import logging
from datetime import datetime

import requests
import boto3
import psycopg2


S3_BUCKET = ''
AWS_REGION = ''

RDS_HOST = ''
RDS_PORT = 5432
RDS_USER = ''
RDS_PASSWORD = ''
RDS_DB = ''

IMAGE_SERVICE_URL = 'https://api.unsplash.com/photos/random'
QUOTE_SERVICE_URL = (
    'https://shakespeare1.p.rapidapi.com/shakespeare/generate/lorem-ipsum'
)


s3_client = boto3.client('s3', region_name=AWS_REGION)


def get_rds_connection():
    return psycopg2.connect(
        host=RDS_HOST,
        port=RDS_PORT,
        user=RDS_USER,
        password=RDS_PASSWORD,
        database=RDS_DB
    )


def upload_to_s3(file_path, s3_bucket, s3_key):
    try:
        s3_client.upload_file(file_path, s3_bucket, s3_key)
        return f"s3://{s3_bucket}/{s3_key}"
    except Exception as e:
        logging.error(f"Error uploading file to S3: {e}")
        raise


def insert_quote_into_rds(quote, img_url):
    conn = get_rds_connection()
    cursor = conn.cursor()
    try:
        send_dt = datetime.now()
        cursor.execute(
            "INSERT INTO quotes (quote, send_dt, img_url) VALUES (%s, %s, %s)",
            (quote, send_dt, img_url)
        )
        conn.commit()
    except Exception as e:
        logging.error(f"Error inserting quote into RDS: {e}")
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()


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


def get_quote():
    url = QUOTE_SERVICE_URL

    headers = {
        'X-RapidAPI-Key': os.getenv('RAPIDAPI_KEY'),
        'X-RapidAPI-Host': 'shakespeare1.p.rapidapi.com'
    }

    response = requests.get(url, headers=headers)

    print(response.json()['contents']['lorem-ipsum'])


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


def send_post_to_teams():
    try:
        image_url = load_random_picture()
    except Exception as e:
        image_url = ""
        print(f'Error occured while loading image: {e}')

    try:
        quote = get_quote()
    except Exception as e:
        quote = ""
        print(f'Error occured while getting quote: {e}')

    try:
        send_to_teams(image_url, quote)
    except Exception as e:
        print(f"Error occured while sending to Teams: {e}")

    try:
        picture_path = ''
        quote = ""

        s3_key = f'/{datetime.now().strftime("%Y/%m/%d/%H%M%S")}.jpg'
        picture_url = upload_to_s3(picture_path, S3_BUCKET, s3_key)

    except Exception as e:
        print(f"Error occured while uploading to s3: {e}")

    try:
        insert_quote_into_rds(quote, picture_url)
    except Exception as e:
        print(f"Error occured while insert quote into rds: {e}")
