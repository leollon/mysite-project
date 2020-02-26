// lib/fetct.js

import fetch from 'isomorphic-unfetch';

export default async function fetcher(url) {
  return fetch(url)
    .then((response) => {
      if (!response.ok) {
        throw new Error(response.status + ' ' + response.statusText);
      }
      return response;
    });
}
