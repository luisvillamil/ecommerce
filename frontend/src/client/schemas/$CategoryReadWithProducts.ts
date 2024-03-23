/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $CategoryReadWithProducts = {
    description: `Inherits from CategoryRead, used to display products from category`,
    properties: {
        name: {
            type: 'string',
            isRequired: true,
        },
        id: {
            type: 'number',
            isRequired: true,
        },
        products: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'ProductRead',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
