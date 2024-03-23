/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemRead = {
    description: `Reading items back, include detailed attribute value information`,
    properties: {
        name: {
            type: 'string',
            isRequired: true,
        },
        description: {
            type: 'string',
        },
        stock_quantity: {
            type: 'number',
            isRequired: true,
        },
        sku: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        product_id: {
            type: 'number',
            isRequired: true,
        },
        price: {
            type: 'number',
            isRequired: true,
        },
        id: {
            type: 'number',
            isRequired: true,
        },
        product: {
            type: 'ProductRead',
            isRequired: true,
        },
        attribute_values: {
            type: 'array',
            contains: {
                type: 'AttributeValueRead',
            },
        },
    },
} as const;
