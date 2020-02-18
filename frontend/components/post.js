// components/post.js

import React from 'react';
import PropTypes from 'prop-types'


export default function ArticleList(props) {
  return (
    <>
      {props.category_name &&
        <blockquote id="category-header">
          有<span className="badge">{statistics}</span>篇文章属于<strong>
            <div className="label label-primary">
              <span className="fa fa-folder-open">
                categoryname
              </span>
            </div>
          </strong>
          分类：
        </blockquote>
      }

      {props.articles ? props.articles.map(article => (
        <div className="post-preview">
          <h2 className="post-title">
            <a href={`/articles/${article.slug}`}>{article.title}</a>
          </h2>
          {/* <article className="post-subtitle">
            <Markdown source={article.article_body} />
          </article> */}
          <div className="article-extra">
              <span className="fa fa-folder">
                <a href={`/categories/${article.category}`}>
                  {article.category}
                </a>
              </span>
              <span className="fa fa-tag"></span>
              {article.tags.split(',').map(tag => (
                <a href={`/tags/${tag}`}>
                  #{tag}
                </a>))}
              
              <span className="fa fa-comments"></span>
              <a href={`/articles/${article.slug}#comments`}>
                <span>
                  comment.count
                </span>
              </a>
              <span className="fa fa-eye"></span>
              <span>{article.user_view_times}</span>
          </div>
            <p className="post-meta">
              Posted by {article.author} on {article.created_time}
            </p>
        </div>))
        : <div className="post-preview">
            <h2 className="post-title">
            暂无文章
            </h2>
        </div>
      }
    </>);
}


ArticleList.propTypes = {
    articles: PropTypes.array.isRequired
}