import { toCamelCase, toSnakeCase } from '../../src/utils';

describe('utils', () => {
    const camelCase = {
        fooBar: 1,
        fooBarArr: [1, 'a', true, { fooBar: 'a' }],
    };
    const snake_case = {
        foo_bar: 1,
        foo_bar_arr: [1, 'a', true, { foo_bar: 'a' }],
    };
    test('camelCaseからcamelCaseに変換', () => {
        expect(toCamelCase(camelCase)).toEqual(camelCase);
    });
    test('camelCaseからsnake_caseに変換', () => {
        expect(toSnakeCase(camelCase)).toEqual(snake_case);
    });
    test('snake_caseからcamelCaseに変換', () => {
        expect(toCamelCase(snake_case)).toEqual(camelCase);
    });
    test('snake_caseからsnake_caseに変換', () => {
        expect(toSnakeCase(camelCase)).toEqual(snake_case);
    });
});
