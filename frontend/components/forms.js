// components/forms.js


export default function CommentForm(props) {

  return (
    <div id="comment-section">
      <p>Leave a comment</p>
      <form id="comment-form" encType="multipart/form-data">
        <div>
          <div className="input">
            <textarea name="comment_text" placeholder="Want to say something?" required id="comment-content" cols="60" rows="10">
            </textarea>
          </div>
          <div className="input">
            <input type="text" id="username" placeholder="Username" required /><span id="username-hint">required</span>
          </div>
          <div className="input">
            <input type="text" id="email" placeholder="Email (not public)" />
          </div>
          <div className="input">
            <input type="text" id="link" placeholder="Link" />
          </div>
          <div className="input">
            <input type="text" id="captcha-input" placeholder="Captcha (required)" required /><span id="catcha-hint">required</span>
            <p><img src="" alt="captcha" id="captcha" /></p>
          </div>
          <div className="input">
            <button type="submit" className="btn" id="comment-submit-btn">Submit</button>
          </div>
        </div>
      </form>
    </div>
  );
}
