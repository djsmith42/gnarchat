var chatRoom = $("#chat-room")
var chatMessageInputBox = $("#chat-input")
var authorNameInputBox = $("#author-name")

function refreshChatMessages() {
    // Fetch chat messages from the server:
  $.getJSON("/messages", function(messages) {
        // Build an HTML string that contains all the messages we got from the server:
        var html = ""
        messages.forEach(function(message) {
          var date = new Date(message.when)
          html += ("<div>" +
            "<button class=\"x-button\" data-id=\"" + message.id + "\">Delete</button> " +
            "<i>" + date.toLocaleTimeString() + "</i> " +
            "<b style=\"color: " + authorToColor(message.author_name) + "\">" + escape(message.author_name) + "</b>: " +
            escape(message.text) + "</div>")
        })

        // Replace all the HTML in the chat room box with the new HTML if it's diferent from the HTML that is already showing:
        if (html != chatRoom.html()) {
            chatRoom.html(html)
            chatRoom.scrollTop(99999999999)
        }

        var allButtons = $(".x-button")
        allButtons.click(function(event) {
            var button = $(event.currentTarget)
            var messageId = button.attr("data-id")
            button.attr("disabled", "disabled")
            $.ajax("/delete_message", {
                contentType: "application/json",
                type: "POST",
                data: JSON.stringify({
                    messageId: messageId
                })
            }).then(function() {
                refreshChatMessages();
            })
        })
    })
}

function authorToColor(authorName) {
  var r = 0, g = 0, b = 0
  var hash = hashCode(authorName)

  // For each digit in the hash, add it to the r, g, or b bucket (with some weird multipliers to increase diversity)
  var digitCount = 0
  var toProcess = hash
  while (toProcess > 0) {
    digitCount++
    var temp = toProcess % 10  * (3 ** digitCount)
    toProcess /= 10
    toProcess |= 0
    switch (digitCount % 3) {
      case 0:
        r += temp
        break;
      case 1:
        g += temp
        break;
      case 2:
        b += temp
    }
  }

  // Make sure each component is between 0 and 255
  r %= 256
  g %= 256
  b %= 256

  // If the color is too light, darken its strongest component
  var luminance = 0.299*r**2 + 0.587*g**2 + 0.114*b**2
  if (luminance > 30000) {
    if (r > g && r > b) {
      r /= 2
    }
    else if (g > r && g > b) {
      g /= 2
    }
    else {
      b /= 2
    }
  }

  // If the color is too dark, brighten one of the components:
  if (luminance < 5000) {
    if (r < g && r < b) {
      r = Math.max(100, r * 2)
    }
    else if (g < r && g < b) {
      g = Math.max(100, g * 2)
    }
    else {
      b = Math.max(100, b * 2)
    }
  }

  r |= 0
  g |= 0
  b |= 0

  return "rgb(" + r + ", " + g + ", " + b + ")"
}

function hashCode(string) {
  // Stolen from: https://stackoverflow.com/questions/7616461/generate-a-hash-from-string-in-javascript-jquery
  var hash = 0
  if (string.length === 0) return hash;
  for (var i = 0; i < string.length; i++) {
    var chr   = string.charCodeAt(i)
    hash  = ((hash << 5) - hash) + chr
    hash |= 0; // Convert to 32bit integer
  }
  return hash;
}

function postMessage(authorName, messageText) {
  return $.ajax("/post_message",  {
    contentType: "application/json",
    type: "POST",
    data: JSON.stringify({
      text: messageText,
      author_name: authorName
    })
  })
}

// This function converts special HTML characters into safe characters,
// so baddies can't make our application execute their nasty code by
// posting chat messages with special HTML characters
function escape(text) {
  return $("<div>").text(text).html()
}

chatMessageInputBox.keypress(function(event) {
  if (event.which == 13) {
    var authorName = authorNameInputBox.val()
    var messageText = chatMessageInputBox.val()
    if (authorName.trim() != '' && messageText.trim() != '') {
      postMessage(authorName, messageText).then(refreshChatMessages)
      chatMessageInputBox.val('')
      localStorage.setItem("authorName", authorName)
    }
  }
})

authorNameInputBox.val(localStorage.getItem("authorName"))
refreshChatMessages()
setInterval(refreshChatMessages, 1000)
