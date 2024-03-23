/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProductReadWithAttributes = {
    description: `Inherits from CategoryRead, used to display products from category`,
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
        id: {
            type: 'number',
            isRequired: true,
        },
        images: {
            type: 'array',
            contains: {
                type: 'Image',
            },
            isRequired: true,
        },
        attributes: {
            type: 'any-of',
            contains: [{
                type: 'array',
                contains: {
                    type: 'AttributeRead',
                },
            }, {
                type: 'null',
            }],
        },
    },
} as const;
