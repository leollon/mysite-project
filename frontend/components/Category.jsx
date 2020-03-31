// components/Category.jsx

import React from 'react'
import PropTypes from 'prop-types'

const label = ['default', 'primary', 'info', 'success', 'warning', 'danger']

export default function CategoryList(props) {
    return (
        <ul id="categories">
            {props.categories.length ? (
                props.categories.map((category) => (
                    <li
                        key={category.name}
                        className={`fa label label-${
                            label[
                                Math.floor((Math.random() * 100) % label.length)
                            ]
                        }`}
                    >
                        <a href={`/categories/${category.name}`}>
                            {category.name}
                        </a>
                        <sup>{category.article_statistics}</sup>
                    </li>
                ))
            ) : (
                <h2 className="empty">
                    <strong>No categories yet!</strong>
                </h2>
            )}
        </ul>
    )
}

CategoryList.propTypes = {
    categories: PropTypes.array.isRequired,
}
