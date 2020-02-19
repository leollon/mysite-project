// static/js/blog.js

const api_host = "http://dev.django.com";

$("#comment_text").on("input", function (event) {
    $("#comment-text-error").removeClass("error").addClass("no-error");
})
$("#username").on("input", function (event) {
    $("#username-error").removeClass("error").addClass("no-error");
})
$("#email").on("input", function (event) {
    $("#email-error").removeClass("error").addClass("no-error")
})
$("#link").on("input", function (event) {
    $("#link-error").removeClass("error").addClass("no-error")
})
$("#captcha-input").on("input", function (event) {
    $("#captcha-error").removeClass("error").addClass("no-error");
})

$('#captcha').ready(setCaptcha);
$('#captcha').click(setCaptcha);

$('.reply').click(function (event) {
    event.preventDefault()
    let commentText = $("#comment_text").val();
    let commenter = '@'.concat(this.dataset.commenter);
    if (commentText && commentText.match(/@[\w\d\ ]+/).length) {
        commentText = commentText.replace(/(@[\w\d]+)/, '').trim();
    }
    if (commentText.indexOf(commenter) < 0) {
        $('#comment_text').val(commenter.concat(" ").concat(commentText));
    }
})

async function sendData(request) {
    const response = await fetch(request)
        .then((response) => {
            if (!response.ok) {
                throw new Error(response.status + ' ' + response.statusText);
            }
            return response;
        });
    return response.json();
}

$("#comment-submit-btn").click(function (event) {
    event.preventDefault();
    let formData = new URLSearchParams(new FormData(document.getElementById("comment-form")));
    const article_slug = $("#comment-form").attr('action');
    const url = api_host + '/api/v1/articles' + article_slug + '/comments/';

    const postCommentReq = new Request(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        body: formData,
        credentials: 'include',
        redirect: 'follow',
    })
    sendData(postCommentReq)
        .then(() => {
            // Reload current page, so that the newest comment can be showed off.
            window.location.reload();
        })
        .catch(error => {
            console.log(error);
        });
})

function setCaptcha() {
    const url = api_host + "/refresh/captcha/";

    $.getJSON(url, function (data) {
        $("#captcha").attr("src", api_host + data.captchaImgPath);
        $("#csrftoken").attr("value", data.CSRFToken);
    })
}