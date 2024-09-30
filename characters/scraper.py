import requests

from characters.models import Character
from django.conf import settings


def scrape_characters() -> list[Character]:
    next_url_to_scrape = settings.RICK_AND_MORTY_API_CHARACTERS_URL

    characters = []

    while next_url_to_scrape is not None:
        characters_response = requests.get(next_url_to_scrape).json()

        for characters_dict in characters_response["results"]:
            characters.append(
                Character(
                    api_id=characters_dict["id"],
                    name=characters_dict["name"],
                    status=characters_dict["status"],
                    species=characters_dict["species"],
                    gender=characters_dict["gender"],
                    image=characters_dict["image"],
                )
            )

        next_url_to_scrape = characters_response["info"]["next"]

    return characters


def save_characters(characters: list[Character]) -> None:
    for character in characters:
        character.save()


def sync_characters_with_api() -> None:
    characters = scrape_characters()
    save_characters(characters)
