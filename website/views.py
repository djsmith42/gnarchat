import json
from django.http import HttpResponse
from .models import ChatMessage

def index(request):
    # This function returns the main HTML page for the chat app:
    return HttpResponse("""
    <html>
        <head>
            <style>
            p {
                margin: 0;
            }
            #chat-room {
                border: 1px solid black;
                padding: 10px;
                min-height: 500px;
                max-height: 500px;
                overflow-y: auto;
            }
            #chat-input {
                padding: 5px;
                width: 100%;
                border: 1px solid black;
                border-top: none;
            }
            </style>
        </head>

        <body>
            <h1>It's Gnarchat!</h1>
            <div>
            	<input type="text" id="author-name" placeholder="Enter your name" />
            </div>
            <div id="chat-room">
            </div>
            <div>
                <input type="text" id="chat-input" placeholder="Chat message here" />
            </div>
            <h2>And now, some info about narwhals!</h2>
                <input type="text" value="welcome you have entered the world of narwhals, you must not say anything bad about narwhals"/>

            <img src="static/gnarwhal.jpg" style="width: 500px" />
            <img src="static/dgnarwhal.jpg" style="width: 500px" />
            <p>Narwhals, the Unicorns of the Sea</p>
            <p>&nbsp; &nbsp; (🐳)&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;(🦄)&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;&nbsp; &nbsp;(🌊) </p>

    Narwhals are, by far, the best animals on earth. They are awesome, have one huge tusk on their nose (more on that later),
and a whole fan club, who wrote the page you are now reading. And made the website you are now on.
And named it Gnarchat after Gnarly Narwhals, because WHY NOT. But now I will get to the point, and teach you about narwhals.
The saddest thing that exists is somebody who is undereducated about narwhals. Some people don’t even know they exist, and other think that they are fantasy,
right up there with the phoenix and unicorns. Here are ten fun facts about narwhals:
<li>1. They are “near threatened” on the list of endangerment </li>
<li>2. The mass of an adult narwhal can reach 2,100 pounds</li>
<li>3. The scientific name for a narwhal is Monodon monoceros</li>
<li>4. This translates to ‘One tooth, one horn’</li>
<li>5. Narwhals are carnivorous</li>
<li>6. An adult narwhal can reach 17 feet long</li>
<li>7. Narwhals generally move slowly, but when being chased by predators, they can move very quickly</li>
<li>8. Mature female narwhals will have a calf about every three years</li>
<li>9. Narwhals do not have dorsal fins</li>
<li>10. Narwhals have a thick layer of blubber that allows them to swim in very cold water</li>
Here are three fun facts about the tusk:
<li>1. Generally, only male narwhals have tusks</li>
<li>2. Sometimes a female is born with a tusk</li>
<li>3. It is very rare, but sometimes there is a narwhal with two tusks</li>
________________________________________   !   ________________________________________</p>
        	<img src="static/narwhal-skull-with-tusk-24.jpg">
        <br/>
        <input type="text"/>
        </body>
        <script type="text/javascript" src="https://code.jquery.com/jquery-latest.min.js"></script>
        <script type="text/javascript" src="/static/chat.js"></script>
    </html>
    """)

def messages(request):
    max_message_count = 100

    # Fetch the chat messages from the database:
    chat_messages = list(reversed(list(ChatMessage.objects.order_by('-when')[:max_message_count].values())))

    # Convert each date to a string so we can send it over JSON to the browser (JSON doesn't support date/time)
    for chat_message in chat_messages:
        chat_message['when'] = chat_message['when'].isoformat()

    # Send them to the browser:
    return HttpResponse(json.dumps(chat_messages), content_type="application/json")

def delete_message(request):
    # Parse the chat message info from the browser request:
    payload = json.loads(request.body)
    message_id = payload["messageId"]

    # Store the chat message in the database:
    ChatMessage.objects.filter(id=message_id).delete()

    # Return an empty response to tell the browser it worked:
    return HttpResponse("")

def post_message(request):
    # Parse the chat message info from the browser request:
    payload = json.loads(request.body)

    # Store the chat message in the database:
    ChatMessage.objects.create(text=payload["text"], author_name=payload["author_name"])

    # Return an empty response to tell the browser it worked:
    return HttpResponse("")
