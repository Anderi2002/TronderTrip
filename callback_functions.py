from destination import Destination
from mail_bot import send_mail
from config import target_email, sender_email, name
from keys import app_password
from datetime import datetime


def accepted_trip(destination: Destination, destinations_info: dict[str: str | int]) -> None:
    date = ".".join((str(datetime.now().date()).split("-")[::-1]))
    # Construct mail
    subject: str = f"Turforslag - {destination.name} | {date}"
    
    rain: int = destinations_info[destination.name]['rain']
    rain_arg = "Det er ikke meldt noe regn!" if not rain else f"Det er meldt {rain} mm regn"
    if rain:
        rain_arg_2 = ", så her kan det være lurt å ha med regnjakke!" if rain > 10 else "."
        rain_arg += rain_arg_2

    body: str = fr"""
    <html>
        <head></head>
        <body>
            <p>Hei {name}!<br>
                Dagens turforslag er <b>{destination.name}</b>!<br>
                Det er meldt {destinations_info[destination.name]['temperature']} °C.
                {rain_arg}
            </p>
            <p>
                Informasjon om turen finner du vedlagt;<br>
                <a href="{destinations_info[destination.name]['google_maps_link']}">Google Maps - {destination.name}</a><br>
                <a href="{destinations_info[destination.name]['yr_link']}">Yr - {destination.name}</a>
            </p>
            <p>
                God Tur! <3
                <img src="{destination.image_url}" alt="Image of {destination.name}">
            </p>
        </body>
    </html>
    """

    send_mail(subject, body, sender_email, target_email, app_password, html = True)
