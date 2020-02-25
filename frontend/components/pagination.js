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

  if (previous || next) {
    return (
      <ul className="pager">
        <li className={`previous${previous ? '' : ' disabled'}`} key="previous">
          <Link href={previous ? previous : '#'} as={`${previous ? previous : '#'}`}>
            <a>&larr; Newer</a>
          </Link>
        </li>
        <li className={`next${next ? '' : ' disabled'}`} key="next">
          <Link href={next ? next : '#'} as={`${next ? next : '#'}`}>
            <a>Older &rarr;</a>
          </Link>
        </li>
      </ul>);
  }
  return null;
}


PageList.propTypes = {
    links: PropTypes.object.isRequired,
}