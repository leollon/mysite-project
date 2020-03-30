// jest.config.js

const { defaults } = require('jest-config')

module.exports = {
    moduleFileExtensions: [...defaults.moduleFileExtensions, 'ts', 'tsx'],
    transform: {
        '.+\\.[t|j]sx?$': 'babel-jest',
    },
}
