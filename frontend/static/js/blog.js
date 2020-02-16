// static/js/blog.js

const api_host = "http://dev.django.com"
const commentSubmitButton = document.getElementById("comment-submit-btn");

document.addEventListener('DOMContentLoaded', (event) => { getCaptcha();})
document.getElementById('captcha').addEventListener('click', (event) => (getCaptcha()));

function getCaptcha() {
  let xhRequest = new XMLHttpRequest();
  xhRequest.onloadend = setCaptcha;
  xhRequest.open("GET", api_host + "/refresh/captcha/", true);
  xhRequest.send();
}

function setCaptcha() {
  const response = JSON.parse(this.responseText);
  document.getElementById("captcha").src = api_host + response.captchaImgPath;
  document.getElementById("csrftoken").value = response.CSRFToken;
}

commentSubmitButton.addEventListener('click', function (event) {
  event.preventDefault();
  let formData = new FormData(document.getElementById("comment-form"));
  const xhRequest = new XMLHttpRequest();
  xhRequest.onloadend = function (event) { window.location.reload(); };
  xhRequest.open("POST", api_host + '/api/v1/articles/hello-world/comments/', true);
  xhRequest.send(formData);
})
