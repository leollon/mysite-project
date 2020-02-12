// components/tag.js

import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types'


export default function TagList(props) {
  return (
    <ul>
      {Object.entries(props.tags).map(array => (
        <li key={array[0]}>
          <Link href="/tags/[name]" as={`/tags/${array[0]}`}>
            <a>{array[0]}<sup>{array[1]}</sup></a>
          </Link>
        </li>))
      }
    </ul>
  );
}


TagList.propTypes = {
    tags: PropTypes.object
}
