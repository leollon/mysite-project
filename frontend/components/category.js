// components/category.js

import React from 'react';
import Link from 'next/link';
import PropTypes from 'prop-types'

export default function CategoryList(props) {
    return (
        <ul>
            {props.categories.map(category => (
                <li key={category.name}>
                    <Link href="/categories/[name]" as={`/categories/${category.name}`}>
                        <a>{category.name}</a>
                    </Link>
                    
                </li>))
            }
        </ul>
    );
}

CategoryList.propTypes = {
    categories: PropTypes.object.isRequired
}