// utils/helpers.js

import fetch from 'isomorphic-unfetch';

function checkStatus(response) {
    if (response.ok) {
        return response;
    } else {
        var error = new Error(response.statusText);
        error.response = response;
        return Promise.reject(error);
    }
};


export default async function fetcher(url) {
    return fetch(url)
        .then(checkStatus)
        .then(r => r.json());
};
