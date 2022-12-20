from destination import Destination
from mail_bot import send_mail
from config import target_email, sender_email, name
from keys import app_password


def accepted_trip(destination: Destination, destinations_info: dict[str: str | int]) -> None:
    # Construct mail
    subject: str = f"Turforslag - {destination.name}"

    body: str = f"""
    Hei {name}!
    Dagens tur er {destination.name}!
    Det er meldt {destinations_info[destination.name]['temperature']} °C.\n
    Informasjon om turen finner du vedlagt;
    Google Maps: {destinations_info[destination.name]['google_maps_link']}
    Yr: {destinations_info[destination.name]['yr_link']}\n
    God tur!
    """

    send_mail(subject, body, sender_email, target_email, app_password)
    print(f"Mail sent to {target_email}")
