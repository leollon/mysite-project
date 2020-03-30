module.exports = {
    env: {
        test: {
            presets: [
                [
                    '@babel/preset-env',
                    {
                        targets: {
                            node: 'current',
                        },
                    },
                ],
                '@babel/preset-react',
            ],
            plugins: [],
        },
        development: {
            presets: [
                [
                    'next/babel',
                    {
                        'preset-env': {
                            targets: {
                                node: 'current',
                            },
                        },
                    },
                ],
            ],
            plugins: [],
        },
        production: {
            presets: [
                [
                    'next/babel',
                    {
                        'preset-env': {
                            targets: {
                                node: 'current',
                            },
                        },
                    },
                ],
            ],
            plugins: [],
        },
    },
}
