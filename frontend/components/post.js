// components/post.js

import React from 'react';
import PropTypes from 'prop-types'


export default function ArticleList(props) {
  return (
    <>
      <h1>My blog</h1>
      <ul id="article-list">
        {props.articles.map(article => (
          <li key={article.title} className="article">
              <a href={`/articles/${article.slug}`}>{article.title}</a>
          </li>
          ))}
      </ul>
    </>
  );
}


ArticleList.propTypes = {
    articles: PropTypes.array.isRequired
}