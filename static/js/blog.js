'use strict';
if ($('#article-editor')[0] !== 'undefined') {
    $("#menu-toggle").trigger("click");
};

function markdownToHtmlHandler(text) {
    var converter = new showdown.Converter();
    converter.setFlavor('github');
    return converter.makeHtml(text);
}

$('#id_title').on('input', function () {
    $('#article-title').text($('#id_title').val());
})

$('#id_article_body').on('input', function () {
    $('#article-preview-body').html(markdownToHtmlHandler($('#id_article_body').val()));
})

function comment_input(username) {
    var commentText = $('#id_comment_text').val();
    $('#id_comment_text').val('@'.concat(username).concat(" ") + commentText);
}

function createXhrObject() {
    return new XMLHttpRequest();
}

function clear_input(eleArray) {
    for (var i = 0; i < eleArray.length; ++i) {
        document.getElementsByName(eleArray[i])[0].value = '';
    }
}

function postComment(post_id) {
    var xhRequest = createXhrObject();
    var url = '/api/comment/';
    var data = {
        "username": document.getElementsByName("username")[0].value,
        "email": document.getElementsByName("email")[0].value,
        "link": document.getElementsByName("link")[0].value,
        "comment_text": document.getElementsByName("comment_text")[0].value,
        "post": post_id
    }
    var eleArray = ["username", "email", "link", "comment_text"];
    var json = JSON.stringify(data);
    clear_input(eleArray);
    xhRequest.onreadystatechange = function () {
        if (xhRequest.readyState == 4 && xhRequest.status == "201") {
            // reload the current whole page to get latest comment seen.
            document.location.reload(true);
        }
    };
    let csrfToken = $("[name=csrfmiddlewaretoken]").val();
    xhRequest.open("POST", url, true);
    xhRequest.setRequestHeader("Content-type", "application/json; charset=utf-8");
    xhRequest.setRequestHeader("X-CSRFToken", csrfToken);
    xhRequest.send(json);
}

function getCookie() {
    var cookie = document.cookie;
    var fieldList = cookie.split(";");
    for (var i in fieldList) {
        var field = fieldList[i].split("=");
        if (field[0].trim() === "csrftoken") {
            return field[1].trim();
        }
    }
}