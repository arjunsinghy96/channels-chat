import json

def message_websocket_json(message):
    """
    Generates a json encoded dictionory to be sent via websocket.
    The json schema is as follows:
    {
        type: "message:new",
        content: {
            message: {
                type: "text" or "image",
                src: "/media/images/some_images.jpg", # only for images
                text: "hello world. bla bla bla", # only for text type
                league: "slug-of-league",
                sender: "username",
                sent_at: "Apr 04 2018, 16:12 PM",
            }
        }
    }

    :param message: A Message object
    :return: Dictionary object
    """
    data = {
        "type": "message:new",
        "content": {
            "message": {
                "type": "text",
                "text": message.message,
                "league": message.league.slug,
                "sender": message.sender.username,
                "sent_at": message.sent_at.strftime('%b %m %Y, %H:%M %p')
            }
        }
    }
    return json.dumps(data)