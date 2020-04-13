// components/Pagination.jsx

import React from 'react';
import PropTypes from 'prop-types';

function getCursor(link) {
    const linkRegExp = /\?cur=[\w=%]+/g;
    const results = linkRegExp.exec(link);
    return results ? results[0] : undefined;
}

export default function PageList(props) {
    const previous = getCursor(props.links.previous);
    const next = getCursor(props.links.next);

    if (previous || next) {
        return (
            <ul className="pager">
                <li
                    className={`previous${previous ? '' : ' disabled'}`}
                    key="previous"
                >
                    <a href={previous ? previous : '#'}>&larr; Newer</a>
                </li>
                <li className={`next${next ? '' : ' disabled'}`} key="next">
                    <a href={next ? next : '#'}>Older &rarr;</a>
                </li>
            </ul>
        );
    }
    return null;
}

PageList.propTypes = {
    links: PropTypes.object.isRequired,
};
