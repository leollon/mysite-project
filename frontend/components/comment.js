// pages/articles/[slug]/comments.js

import ReactMarkdown from 'react-markdown';

import PageList from './pagination';


export default function Comments(props) {

  return (
    <div>
      <h3>Comment list</h3>
      <ul>
        {props.comments.results.map(comment => (
          <li className="comment-text" key={comment.username + comment.created_time}>
            <div><a href={comment.link ? comment.link : ''} className="author">{comment.username}:</a></div>
            <div className="content"><ReactMarkdown source={comment.comment_text} /></div>
            <a href={'#' + comment.username} className="timestamp">{comment.created_time}</a>
          </li>))}
      </ul>
      <PageList links={props.comments.links} />
    </div>
  );
}
