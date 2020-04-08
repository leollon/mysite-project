// static/js/blog.js

const api_host = 'http://prod.django.com';

$('#captcha').ready(setCaptcha);
$('#captcha').click(setCaptcha);

$('#comment_text').on('input', function (event) {
    $('#comment-text-error').removeClass('error').addClass('no-error');
});
$('#username').on('input', function (event) {
    $('#username-error').removeClass('error').addClass('no-error');
});
$('#email').on('input', function (event) {
    $('#email-error').removeClass('error').addClass('no-error');
});
$('#link').on('input', function (event) {
    $('#link-error').removeClass('error').addClass('no-error');
});
$('#captcha-input').on('input', function (event) {
    $('#captcha-error').removeClass('error').addClass('no-error');
});

$('.reply').click(function (event) {
    event.preventDefault();
    let commentText = $('#comment_text').val();
    let commenter = '@'.concat(this.dataset.commenter);
    if (commentText && commentText.match(/@[\w\d\s]+/).length) {
        commentText = commentText.replace(/(@[\w\d]+)/, '').trim();
    }
    if (commentText.indexOf(commenter) < 0) {
        $('#comment_text').val(commenter.concat(' ').concat(commentText));
    }
});

async function sendRequest(request) {
    const response = await fetch(request).then((response) => {
        // Check where the fetch request was successful not.
        if (!response.ok) {
            throw new Error(response.status + ' ' + response.statusText);
        }
        return response;
    });
    return response.json();
}

$('#comment-submit-btn').click(function (event) {
    event.preventDefault();
    let formData = new URLSearchParams(
        new FormData(document.getElementById('comment-form'))
    );
    const article_slug = $('#comment-form').attr('action');
    const url = api_host + '/api/v1/articles' + article_slug + '/comments/';

    const postCommentReq = new Request(url, {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        body: formData,
        credentials: 'include',
        redirect: 'follow',
    });
    sendRequest(postCommentReq)
        .then(() => {
            // Reload current page, so that the newest comment can be showed off.
            window.location.reload();
        })
        .catch((error) => {
            alert(error.message);
        });
});

function setCaptcha() {
    const url = api_host + '/api/v1/refresh/captcha/';

    const getCaptchaReq = new Request(url);
    sendRequest(getCaptchaReq)
        .then((responseData) => {
            $('#captcha-error').addClass('no-error').removeClass('error');
            $('#captcha').attr('src', api_host + responseData.captchaImgPath);
            $('#csrftoken').attr('value', responseData.CSRFToken);
        })
        .catch((error) => {
            $('#captcha-error')
                .removeClass('no-error')
                .addClass('error')
                .text("Can't get the captcha");
        });
}
