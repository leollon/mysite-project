var is_post_detail_page = window.location.href.split('/').indexOf('post');
var is_editor_page = document.getElementById('article-editor');


if (is_post_detail_page && !is_editor_page) {
    document.getElementById('blog-head').innerHTML = document.getElementById('article-title').innerHTML;
//    console.log(is_editor_page);  // for test
}

function markdownToHtmlHandler(text) {
    'use strict';
    var converter = new showdown.Converter();
    converter.setFlavor('github');
    return converter.makeHtml(text);
}

// 这里后期可能要做监听事件的监听策略了，监听了不必要的事件了，比如监听单选框的输入了
window.addEventListener('input', function editorPage() {
    'use strict';
//    console.log('hello, showdown'); // for test user input
    if (is_editor_page) {
        //  preview                                                  editor
        document.getElementById('article-title').innerHTML = document.getElementById('id_title').value;
        document.getElementById('article-preview-body').innerHTML = markdownToHtmlHandler(document.getElementById('id_article_body').value);
    }
})

function comment_input(username) {
    document.getElementById('id_comment_text').innerText += '@'.concat(username).concat(" ");
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
