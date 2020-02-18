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
    <ul class="pager">
      {previous &&
        <li class="previous">
          <Link href={previous} as={`${previous}`}>
            <a href={previous}>&larr; Newer Posts</a>
          </Link>
        </li>}
      {next &&
        <li class="next">
          <a href={next}>Older Posts &rarr;</a>
        </li>}
    </ul>
  );
}

PageList.propTypes = {
    links: PropTypes.object.isRequired,
}