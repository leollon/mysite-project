// components/Forms.jsx

import React from 'react'
import PropTypes from 'prop-types'

export default function CommentForm(props) {
    return (
        <div>
            <p>Leave a comment</p>
            <form
                className="form-inline"
                action={`/${props.slug}`}
                method="post"
                encType="multipart/form-data"
                id="comment-form"
            >
                <input
                    type="hidden"
                    id="post"
                    name="post"
                    value={props.post_id}
                />
                <input
                    type="hidden"
                    id="csrftoken"
                    name="csrfmiddlewaretoken"
                    value=""
                />
                <div className="container-fluid">
                    <div className="row">
                        <div className="col-xs-12 col-sm-12 col-md-12 col-lg-12 input-box comment-form-input">
                            <textarea
                                name="comment_text"
                                id="comment_text"
                                placeholder="Want to say something?"
                                required
                                cols="60"
                                rows="10"
                            />
                            <p
                                className="small text-muted no-error"
                                id="comment-text-error"
                            />
                        </div>
                        <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4 input-box comment-form-input">
                            <input
                                type="text"
                                name="username"
                                id="username"
                                placeholder="Username (required)"
                                required
                            />
                            <p
                                className="small text-muted no-error"
                                id="username-error"
                            />
                        </div>
                        <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4 input-box comment-form-input">
                            <input
                                type="text"
                                name="email"
                                id="email"
                                placeholder="Email (not public)"
                            />
                            <p
                                className="small text-muted no-error"
                                id="email-error"
                            />
                        </div>
                        <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4 input-box comment-form-input">
                            <input
                                type="text"
                                name="link"
                                placeholder="Link"
                                id="link"
                            />
                            <p
                                className="small text-muted no-error"
                                id="link-error"
                            />
                        </div>
                        <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4 comment-form-input">
                            <img id="captcha" alt="captcha" src="" />
                            <p
                                className="small text-muted no-error"
                                id="captcha-error"
                            />
                        </div>
                        <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4 input-box comment-form-input">
                            <input
                                type="text"
                                id="captcha-input"
                                name="captcha"
                                placeholder="Captcha (required)"
                                required
                            />
                            <p
                                className="small text-muted no-error"
                                id="captcha-input-error"
                            >
                                Fill the captcha.
                            </p>
                        </div>
                        <div className="col-xs-12 col-sm-4 col-md-4 col-lg-4 comment-form-input">
                            <button
                                type="submit"
                                id="comment-submit-btn"
                                className="btn btn-default"
                            >
                                Submit Comment
                            </button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    )
}

CommentForm.propTypes = {
    slug: PropTypes.string.isRequired,
    post_id: PropTypes.number.isRequired,
}
