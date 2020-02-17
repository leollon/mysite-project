// components/forms.js


export default function CommentForm(props) {

  return (
    <div id="comment-section">
      <h3>Leave a comment</h3>
      <form id="comment-form" encType="multipart/form-data" method="post">
        <div>
          <div className="form-input">
            <textarea name="comment_text" placeholder="Want to say something?" required id="comment-content-input" cols="60" rows="10">
            </textarea>
          </div>
          <div className="form-input">
            <input type="text" name="username" id="username" placeholder="Username" required /><span id="username-hint"> required</span>
          </div>
          <div className="form-input">
            <input type="text" id="email" placeholder="Email (not public)" />
          </div>
          <div className="form-input">
            <input type="text" id="link" placeholder="Link" />
          </div>
          <div className="form-input">
            <input type="text" id="captcha-input" name="captcha" placeholder="Captcha (required)" required /><span id="catcha-hint"> required</span>
            <p><img src="" alt="captcha" id="captcha" /></p>
          </div>
          <div className="form-input">
            <button type="submit" className="btn" id="comment-submit-btn">Submit</button>
          </div>
          <input type="hidden" id="post" name="post" value={props.post_id} />
          <input type="hidden" id="csrftoken" name="csrfmiddlewaretoken" value="" />
        </div>
      </form>
    </div>
  );
}
