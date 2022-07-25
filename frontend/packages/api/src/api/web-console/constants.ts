import { Method } from 'axios';

/* eslint-disable */
export const BASE_URI = process.env.VUE_APP_CONSOLE_API_URL;
export const AUTH_TOKEN_API_URI = '/auth/token/';

export const METHOD = {
    GET: 'GET' as Method,
    POST: 'POST' as Method,
    PUT: 'PUT' as Method,
    DELETE: 'DELETE' as Method,
};

/* eslint-enable */
