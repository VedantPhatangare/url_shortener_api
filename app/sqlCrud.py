from .db import db_connect
import random, string


def longToshort(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def addShortUrl(long_url:str):
    connection = db_connect()
    cursor = connection.cursor()
    short_url = longToshort()

    try:
        cursor.execute(
            "INSERT INTO urls (long_url,short_url) VALUES (%s,%s) RETURNING short_url",
            (long_url,short_url)
        )
        connection.commit()
        return short_url
    finally:
        cursor.close()
        connection.close()


def get_url_by_short(short_url: str):
    connection = db_connect()
    cursor = connection.cursor()

    try:
        cursor.execute("SELECT long_url FROM urls WHERE short_url = %s",(short_url,))
        result = cursor.fetchone()
        return result[0] if result else None
    finally:
        cursor.close()
        connection.close()