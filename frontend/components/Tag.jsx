// components/Tag.jsx

import React from 'react'
import PropTypes from 'prop-types'

export default function TagList(props) {
    const label = ['default', 'primary', 'info', 'success', 'warning', 'danger']
    return (
        <ul id="tags">
            {props.count ? (
                Object.entries(props.tags).map((array) => (
                    <li
                        key={array[0]}
                        className={`label label-${
                            label[
                                Math.floor((Math.random() * 100) % label.length)
                            ]
                        }`}
                    >
                        <a href={`/tags/${array[0]}`}>{array[0]}</a>
                        <sup>{array[1]}</sup>
                    </li>
                ))
            ) : (
                <h2 className="empty">
                    <strong>No tags yet!</strong>
                </h2>
            )}
        </ul>
    )
}

TagList.propTypes = {
    tags: PropTypes.object.isRequired,
    count: PropTypes.number.isRequired,
}
