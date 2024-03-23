/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProductCreate = {
    description: `Used by api to create products.
    extra attributes are appeneded by create_product function in db`,
    properties: {
        name: {
            type: 'string',
            isRequired: true,
        },
        description: {
            type: 'string',
            isRequired: true,
        },
        category_id: {
            type: 'number',
        },
        attributes: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'AttributeCreate',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
