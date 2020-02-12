// components/post.js

import React from 'react';
import PropTypes from 'prop-types'


export default function ArticleList(props) {
  return (
    <>
      <h1>My blog</h1>
      <ul>
        {props.articles.map(article => (
          <li key={article.title}>
              <a href={`/articles/${article.slug}`}>{article.title}</a>
          </li>
          ))}
      </ul>
    </>
  );
}


ArticleList.propTypes = {
    articles: PropTypes.object.isRequired
}