// __tests__/components/Category.test.jsx

import React from 'react';
import { render, unmountComponentAtNode } from 'react-dom';
import CategoryList from '../components/Category';

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

describe('renders category component', () => {
    it('renders with empty category', () => {
        const categories = [];

        render(<CategoryList categories={categories} />, container);
        expect(container.textContent).toBe('No categories yet!');
    });

    it('renders with more than one category', () => {
        const categories = [
            { name: 'category-a', article_statistics: 0 },
            { name: 'category-b', article_statistics: 10 },
            { name: 'category-c', article_statistics: 110 },
        ];

        render(<CategoryList categories={categories} />, container);
        expect(container.textContent).toContain('category-a');
    });
});
