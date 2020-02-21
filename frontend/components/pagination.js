// components/pagination.js

import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types'


function getCursor(link) {
  const linkRegExp = /\?cur=[\w=%]+/g;
  const results = linkRegExp.exec(link);
  return (results ? results[0] : undefined);
}


export default function PageList(props) {
  const previous = getCursor(props.links.previous);
  const next = getCursor(props.links.next);
  return (
    <ul className="pager">
      <li className={`previous ${previous ? '' : 'disabled'}`} key="previous">
        <Link href={previous ? previous : '#'} as={`${previous ? previous : '#'}`}>
          <a href={previous}>&larr; Newer</a>
        </Link>
      </li>
      <li className={`next ${next ? '' : 'disabled'}`} key="next">
        <Link href={next ? next : '#'} as={`${next ? next : '#'}`}>
          <a href={next}>Older &rarr;</a>
        </Link>
      </li>
    </ul>
  );
}

PageList.propTypes = {
    links: PropTypes.object.isRequired,
}