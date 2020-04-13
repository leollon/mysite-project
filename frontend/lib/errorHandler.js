// lib/errorHandler.js

export default function handler(error) {
    if (error.name === 'FetchError') {
        return '500 Server Error';
    } else if (error.name === 'AbortError') {
        return 'Request Cancelled';
    } else {
        return error.message;
    }
}
