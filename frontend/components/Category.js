// components/Category.js

import Link from 'next/link';


export default CategoryList = (props) => {
    return (
        <ul>
            {props.categories.map(category => (
                <li>
                    <Link href="/categories/[name]" as={`/categories/${category.name}`}>
                        <a>{category.name}</a>
                    </Link>
                    
                </li>))
            }
        </ul>
    );
};
