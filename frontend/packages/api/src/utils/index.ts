import {
    camelCase,
    isArray,
    isObject,
    List,
    mapKeys,
    mapValues,
    snakeCase,
} from 'lodash';

const mapKeyDeep = (data: unknown, callback: unknown): unknown => {
    if (isArray(data)) {
        return data.map((innerData) => mapKeyDeep(innerData, callback));
    } else if (isObject(data)) {
        return mapValues(
            mapKeys(data as List<unknown>, callback as any),
            (val) => mapKeyDeep(val, callback)
        );
    } else {
        return data;
    }
};

/**
 * オブジェクトのkeyをcamelCaseに変換する
 * @param data camelCaseに変換するオブジェクト
 * @returns camelCaseに変換されたオブジェクト
 */
const toCamelCase = <T = any, U = any>(data: T): U => {
    return mapKeyDeep(data, (value: unknown, key: string) => {
        return camelCase(key);
    }) as U;
};

/**
 * オブジェクトのkeyをsnake_caseに変換する
 * @param data snake_caseに変換するオブジェクト
 * @returns snake_caseに変換されたオブジェクト
 */
const toSnakeCase = <T = any, U = any>(data: T): U => {
    return mapKeyDeep(data, (value: unknown, key: string) => {
        return snakeCase(key);
    }) as U;
};

export { toCamelCase, toSnakeCase };
