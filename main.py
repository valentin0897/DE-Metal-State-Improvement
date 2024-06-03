from utils import load_random_picture
from utils import get_quote
from utils import send_to_teams


def main():
    image_url = load_random_picture()
    quote = get_quote()
    send_to_teams(image_url, quote)


main()
