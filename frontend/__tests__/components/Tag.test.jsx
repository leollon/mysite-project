// __tests__/components/Tag.text.jsx

import React from 'react'
import { render, unmountComponentAtNode } from 'react-dom'
import TagList from '../../components/Tag'

let container = null;

beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
})

afterEach(() => {
    unmountComponentAtNode(container);
    container.remove();
    container = null;
})


it('renders tag component', () => {
    
    let tagData = { count: 0, tags: {} };
    
    // have no tag
    render(<TagList tags={tagData.tags} count={tagData.count} />, container)

    expect(container.querySelector('strong').textContent).toBe('No tags yet!');

    // have only one tag
    tagData = { count: 1, tags: { untagged: 1 } };

    render(<TagList tags={tagData.tags} count={tagData.count} />, container);

    expect(container.querySelector('a').textContent).toBe('untagged');

    // have more than one tag
    tagData = {
        count: 10,
        tags: {
            tag1: 1, tag2: 2, tag3: 3, tag4: 4, tag5: 5, tag7: 7, tag8: 8, tag9: 9, tag0: 10, tag6: 66
        }
    };

    render(<TagList tags={tagData.tags} count={tagData.count} />, container);

    expect(container.querySelector('a').textContent).toBe('tag1');
    expect(container.querySelector('sup').textContent).toBe('1');
})
