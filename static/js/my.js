var splited_url = window.location.href.split('/');
var is_post_detail_page = splited_url.indexOf('post');
var is_editor_page = document.getElementById('article-editor');


if (is_post_detail_page && !is_editor_page) {
    var head = document.getElementById('blog-head');
    head.innerHTML = document.getElementById('article-title').innerHTML;
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

        // editor
        var id_title = document.getElementById('id_title');
        var id_article_body = document.getElementById('id_article_body');

        //  preview
        var article_title_preview = document.getElementById('article-title');
        var article_body_preview = document.getElementById('article-preview-body');
        article_title_preview.innerHTML = id_title.value;
        article_body_preview.innerHTML  = markdownToHtmlHandler(id_article_body.value);
    }
})

function comment_input(username) {
    document.getElementById('id_comment_text').innerText += '@'.concat(username).concat(" ");
}


function createXhrObject() {
    return new XMLHttpRequest();
}

function clear_input() {
    document.getElementsByName("username")[0].value='';
    document.getElementsByName("email")[0].value = '';
    document.getElementsByName("link")[0].value ='';
    document.getElementsByName("comment_text")[0].value;
}
function postComment(post_id) {
    var xhRequest = createXhrObject();
    var url = '/comment/new/';
    var data = {
        "username": document.getElementsByName("username")[0].value,
        "email": document.getElementsByName("email")[0].value,
        "link": document.getElementsByName("link")[0].value,
        "comment_text": document.getElementsByName("comment_text")[0].value,
        "post": post_id
    }
    clear_input();
    var json = JSON.stringify(data);
    xhRequest.onreadystatechange = function() {
        if (xhRequest.readyState == 4 && xhRequest.status == "201") {
            // render new comments from server
        }
    }
    xhRequest.open("POST", url, true);
    xhRequest.setRequestHeader("Content-type", "application/json; charset=utf-8")
    xhRequest.send(json);
}
