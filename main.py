from utils import load_random_picture
from utils import get_quote
from utils import send_to_teams


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
        return


send_post_to_teams()
