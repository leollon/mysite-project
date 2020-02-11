// components/Tag.js

import Link from 'next/link';


export default TagList = (props) => {
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
};
