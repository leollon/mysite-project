// components/Post.js

import React from 'react';
import PropTypes from 'prop-types';
import Markdown from 'react-markdown';


function truncateContent(content, length = 100) {
  if (content.indexOf("。") < length) {
    length = content.indexOf("。")
  }
  return content.substring(0, length) + '....'
}


export default function ArticleList(props) {
  return (
    <>
      {props.articles.length
        ? (props.articles.map(article => {
            const tags = article.tags.split(',');
            return (
              <div key={article.slug} className="post-preview">
                <h2 className="post-title">
                  <a href={`/articles/${article.slug}`}>{article.title}</a>
                </h2>
                <article className="post-subtitle">
                  <Markdown source={truncateContent(article.article_body, 140)} />
                </article>
                <div className="article-extra">
                  <span className="fa fa-folder">
                    <a href={`/categories/${article.category}`}>
                      {article.category}
                    </a>
                  </span>
                    {article.tags.trim(',').split(',').map(tag => (
                      <span key={tag} className="fa fa-tag">
                        <a href={`/tags/${tag}`}>#{tag}</a>
                        {tags.indexOf(tag) !== tags.length - 1 ? ', ' : ''}
                      </span>))}
                  <span className="fa fa-comments">
                    <a href={`/articles/${article.slug}#comments`}>
                      <span>{article.comment_statistics}</span>
                    </a>
                  </span>
                  <span className="fa fa-eye">{article.user_view_times}</span>
                </div>
                <p className="post-meta">
                  Posted by {article.author} on {article.created_time}
                </p>
              </div>)}))
        : (
          <div className="post-preview">
            <h2 className="post-title empty">No Articles yet!</h2>
          </div>)
      }
    </>);
}


ArticleList.propTypes = {
  articles: PropTypes.array.isRequired,
}