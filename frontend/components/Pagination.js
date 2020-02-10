// components/Pagination.js

import Link from 'next/link';


function getCursor(link) {
    const linkRegExp = /\?cur=[\w=%]+/g;
    const results = linkRegExp.exec(link);
    return (results ? results[0] : undefined);
};


export default function PageList(props) {
    const previous = getCursor(props.links.previous);
    const next = getCursor(props.links.next);
    return (
        <ul>
            {previous &&
            <li key={previous}>
                <Link href={previous} as={`${previous}`}>
                    <a>previous</a>
                </Link>
            </li>
            }
            {next && 
                <li key={next}>
                    <Link href={`${next}`}>
                        <a>next</a>
                    </Link>
                </li>
            }
        </ul>
    );
};