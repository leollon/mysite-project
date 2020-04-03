// __tests__/Pagination.test.jsx

import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';

import PageList from '../components/Pagination';

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

describe('renders page list', () => {
    // renderempty page link

    const links1 = { previous: null, next: null };

    it('rendering with empty page link', () => {
        render(<PageList links={links1} />, container);

        expect(container.querySelector('ul')).toBe(null);
    });

    // renders with next link, without previous link
    const links2 = {
        previous: null,
        next:
            'http://example.com/api/v1/articles/?cur=cD0yMDE3LTA4LTIxKzExJTNBMTYlM0EwOCUyQjAwJTNBMDA%3D',
    };

    it('renders with next link, without previous link', () => {
        render(<PageList links={links2} />, container);
        expect(container.querySelector('a').href).toContain('#');
    });

    // renders with previous link, without next link
    const links3 = {
        previous:
            'http://example.com/api/v1/articles/?cur=cj0xJnA9MjAxNy0wOC0yMCswOSUzQTM5JTNBMDIlMkIwMCUzQTAw',
        next: null,
    };

    it('renders with next link, without previous link', () => {
        render(<PageList links={links3} />, container);
        expect(container.querySelector('a').href).toContain('cur');
    });
});
