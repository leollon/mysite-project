// pages/articles/[slug]/comments.js

import ReactMarkdown from 'react-markdown';

import PageList from './pagination';


export default function Comments(props) {

  return (
    <div>
      <ul>
        {props.comments.results.map(comment => (
          <li key={comment.username}>
            <ReactMarkdown source={comment.comment_text} />
            <span className="author">- {comment.username}</span>
          </li>))}
      </ul>
      <PageList links={props.comments.links} />
    </div>
  );
}
