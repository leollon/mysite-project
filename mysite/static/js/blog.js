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

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
        }

    },
    error: function (event) {
        console.log(event);
    }
})

$("#comment-form").submit(function (event) {
    event.preventDefault();
    let formData = new FormData($("#comment-form")[0]);
    if (formData) {
        $.ajax({
            url: '/comment/new/',
            type: 'POST',
            cache: false,
            data: formData,
            enctype: 'multipart/form-data',
            processData: false,
            contentType: "application/x-www-form-urlencoded; charset=UTF-8",
            success: function (data, textStatus, xhr) {
                window.location.reload();
            },
            error: function (xhr, textStatus, errorThrow) {
                console.log(xhr, textStatus, errorThrow)
            }
        })
    }

})

function getCSRFToken() {
    var cookie = $("input[name='csrfmiddlewaretoken']").attr("value");
    return cookie;
}