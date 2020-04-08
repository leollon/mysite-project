// __tests__/Post.test.jsx

import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';
import { create } from 'react-test-renderer';

import ArticleList from '../components/Post';

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

describe('rendering Post component', () => {
    it('renders with empty articles', () => {
        const articles = [];

        render(<ArticleList articles={articles} />, container);
        expect(container.textContent).toBe('No Articles yet!');

        // snapshot testing
        const component = create(<ArticleList articles={articles} />);
        expect(component.toJSON()).toMatchSnapshot();
    });

    it('renders with more than one articles', () => {
        let articles = [
            {
                title: 'abc',
                category: 'ddd',
                author: 'root',
                created_time: '2019-11-16 06:11:19 +0800',
                comment_statistics: 0,
                article_body: 'text content',
                slug: 'abcdads',
                user_view_times: 0,
                tags: 'untagged',
            },
            {
                title: 'cap theory',
                category: 'theory',
                author: 'root',
                created_time: '2019-11-16 06:11:19 +0800',
                comment_statistics: 0,
                article_body: 'Consistency, Availability, Partition tolerance',
                slug: 'cap-theory',
                user_view_times: 0,
                tags: 'cap,分布式系统理论',
            },
            {
                title: 'code',
                category: 'python',
                author: 'root',
                created_time: '2019-11-16 06:11:19 +0800',
                comment_statistics: 0,
                article_body:
                    '```python\n\nprint("hello")\n\nprint("hello")\n\nprint("hello")\n\n```',
                slug: 'code',
                user_view_times: 0,
                tags: 'highlight,dynamic-import',
            },
            {
                title: 'test-head',
                category: 'uncategorized',
                author: 'root',
                created_time: '2019-11-16 06:11:19 +0800',
                comment_statistics: 0,
                article_body: '# head1',
                slug: 'test-head',
                user_view_times: 0,
                tags: 'tag1,tag2,tag3,tag4,tag5',
            },
        ];

        render(<ArticleList articles={articles} />, container);
        // title
        expect(container.textContent).toContain('abc');
        expect(container.textContent).toContain('cap theory');
        expect(container.textContent).toContain('code');
        expect(container.textContent).toContain('test-head');

        // category
        expect(container.textContent).toContain('uncategorized');
        expect(container.textContent).toContain('python');
        expect(container.textContent).toContain('theory');
        expect(container.textContent).toContain('ddd');

        // tag
        expect(container.textContent).toContain('#untagged');
        expect(container.textContent).toContain('#cap, #分布式系统理论');
        expect(container.textContent).toContain('#highlight, #dynamic-import');
        expect(container.textContent).toContain(
            '#tag1, #tag2, #tag3, #tag4, #tag5'
        );

        // snapshot testing
        const component = create(<ArticleList articles={articles} />);
        expect(component.toJSON()).toMatchSnapshot();
    });
});
