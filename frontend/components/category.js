// components/category.js

import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types'


const label = ['default', 'primary', 'info', 'success', 'warning', 'danger']

export default function CategoryList(props) {
  return (
    <ul id="categories">
      {props.categories.length ? (props.categories.map(category => (
        <li key={category.name} className={`fa label label-${label[(Math.floor(Math.random() * 100 % label.length))]}`}>
          <Link href="/categories/[name]" as={`/categories/${category.name}`}>
            <a>{category.name}</a>
          </Link>
          <sup>{category.article_statistics}</sup>
        </li>))): (<h2 class="empty"><strong>No categories yet!</strong></h2>)}
    </ul>
  );
}

CategoryList.propTypes = {
    categories: PropTypes.array.isRequired
}