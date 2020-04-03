// __tests__/component/Comment.test.jsx

import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';

import Comments from '../components/Comment';

let container = null;

beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
});

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
});

describe('rendering comment component', () => {
    // render without comments
    it('renders without comment', () => {
        const commentData = {
            results: [],
            links: { previous: null, next: null },
        };
        render(
            <Comments
                comments={commentData}
                id={1}
                slug={'hello-world'}
                statistics={0}
            />,
            container
        );

        expect(container.textContent).toContain('No Comments yet!');
    });

    // render with one comment
    it('renders with one comment', () => {
        const commentData = {
            results: [
                {
                    created_time: 'Tue, 31 Mar 2020 16:21:16 +0800',
                    username: 'xss',
                    link: '',
                    comment_text: '```python\n\nimport os```',
                },
            ],
            links: { previous: null, next: null },
        };

        render(
            <Comments
                comments={commentData}
                id={2}
                slug={'helloworld'}
                statistics={1}
            />,
            container
        );

        expect(container.textContent).toContain('1 Comment');
    });

    // render with more than one comment
    it('renders with one comment', () => {
        const commentData = {
            results: [
                {
                    created_time: 'Tue, 31 Mar 2020 16:21:16 +0800',
                    username: 'head 1',
                    link: '',
                    comment_text: '# head1',
                },
                {
                    created_time: 'Tue, 31 Mar 2020 16:21:16 +0800',
                    username: 'Python',
                    link: '',
                    comment_text: '```python\n\nimport os```',
                },
                {
                    created_time: 'Tue, 31 Mar 2020 16:21:16 +0800',
                    username: 'xss',
                    link: '',
                    comment_text:
                        '# This is markdown content.\n\n## hello world',
                },
                {
                    created_time: 'Tue, 31 Mar 2020 16:21:16 +0800',
                    username: 'block quote',
                    link: '',
                    comment_text: '# blockquote\n\n> quotation goes here',
                },
            ],
            links: { previous: null, next: null },
        };

        render(
            <Comments
                comments={commentData}
                id={2}
                slug={'helloworld'}
                statistics={1}
            />,
            container
        );

        expect(container.textContent).toContain('head 1');
        expect(container.textContent).toContain('import os');
        expect(container.textContent).toContain('quotation goes here');
    });
});
