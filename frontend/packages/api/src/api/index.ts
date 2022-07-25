import axios, { AxiosInstance } from 'axios';
import { toCamelCase, toSnakeCase } from '../utils';

/**
 * API Client
 * @param baseUrl APIのBaseURL
 * @returns axiosのインスタンス
 */
const api = (baseUrl: string): AxiosInstance => {
    const api = axios.create({ baseURL: baseUrl });
    api.interceptors.request.use(
        (response) => {
            const { data } = response;
            const convertData = toCamelCase(data);
            return { ...response, data: convertData };
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    api.interceptors.response.use(
        (request) => {
            const { data } = request;
            const convertData = toSnakeCase(data);
            return { ...request, data: convertData };
        },
        (error) => {
            return Promise.reject(error);
        }
    );

    return api;
};

export { api };
