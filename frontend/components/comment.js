// pages/articles/[slug]/comments.js

import ReactMarkdown from 'react-markdown';

import CommentForm from './forms';
import PageList from './pagination';


export default function Comments(props) {
  const statistics = props.statistics;
  const comments = props.comments.results;
  const post_id = comments[0] ? comments[0].post : '';
  return (
    <div>
      <h3>{statistics} Comment{statistics != 1 ? 's' : ''}</h3>
      <ul id="comment-list">
        {props.comments.results.map(comment => (
          <li className="comment" key={comment.username + comment.created_time}>
            <div className="image-cropper">
              <img src="/static/img/favicon.png" className="avatar" alt="avatar" />
            </div>
            <div className="comment-content">
              <a href={comment.link ? comment.link : ''} className="author">
                {comment.username + ' '}
              </a>
              <a href={'#' + comment.username} className="timestamp">
                      @ {comment.created_time} :
              </a>
              <ReactMarkdown source={comment.comment_text} />
            </div>
          </li>))}
      </ul>
      <PageList links={props.comments.links} />
      <CommentForm post_id={post_id} />
    </div>
  );
}
