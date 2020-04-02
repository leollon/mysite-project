// jest.config.js

module.exports = {
    testPathIgnorePatterns: ['/node_modules/', '/build/'],
    transform: {'.+\\.[t|j]sx?$': 'babel-jest',},
    transformIgnorePatterns: ['/node_modules/', '/build/',]
}
