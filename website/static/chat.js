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
            "<b>" + escape(message.author_name) + "</b>: " +
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
