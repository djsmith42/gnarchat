from django.shortcuts import render
from django.http import HttpResponse
import json

from .models import ChatMessage

def index(request):
    return HttpResponse("""
    <html>
        <head>
            <style>
            p {
                margin: 0;
            }
            </style>
        </head>

        <body>
            <h1>It's Gnarchat, log in and chat about narwhals!</h1>
            <h2>asdasdf</h2>
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
    payload = list(ChatMessage.objects.order_by('-when').values())
    for chat_message in payload:
        chat_message['when'] = chat_message['when'].isoformat()
    return HttpResponse(json.dumps(payload), content_type="application/json")

def post_message(request):
    message = ChatMessage.objects.create(
        text="this is my message",
        author_name="fake author name",
    )
    return HttpResponse("")
