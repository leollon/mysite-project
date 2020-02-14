// static/js/blog.js

const csrfToken = getCookie('csrftoken');
const commentSubmitButton = document.getElementById("#comment-submit-btn");

document.addEventListener('DOMContentLoaded', (event) => { setCaptcha();})
document.getElementById('captcha').addEventListener('click', (event) => (setCaptcha()));

function setCaptcha() {
  fetch("http://dev.django.com/refresh/captcha/")
    .then((response) => { return response.json() })
    .then((json) => {
      document.getElementById("captcha").src =  'http://dev.django.com' + json.captchaImgPath;
    });
}

function getCookie(name) {
  var cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    var cookies = document.cookie.split(';');
    for (var i = 0; i < cookies.length; i++) {
      var cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
      }
    }
  }
  return cookieValue;
}


