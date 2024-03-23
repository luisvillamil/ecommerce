/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ItemCreate = {
    description: `For creating items, include a list of AttributeValueCreate instances`,
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
        attribute_values: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'AttributeValueCreate',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
