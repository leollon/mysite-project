// components/tag.js

import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types'


export default function TagList(props) {
  const label = ['default', 'primary', 'info', 'success', 'warning', 'danger']
  return (
    <ul id="tags">
      {props.tags ? Object.entries(props.tags).map(array => (
        <li key={array[0]} className={`label label-${label[(Math.floor(Math.random() * 100 % label.length))]}`}>
          <Link href="/tags/[name]" as={`/tags/${array[0]}`}>
            <a>{array[0]}<sup>{array[1]}</sup></a>
          </Link>
        </li>)) : (<h2 class="empty"><strong>No tags yet!</strong></h2>)}
    </ul>
  );
}


TagList.propTypes = {
    tags: PropTypes.object.isRequired
}
