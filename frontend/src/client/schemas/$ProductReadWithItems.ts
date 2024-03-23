/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProductReadWithItems = {
    description: `Update the Product models to include items with attributes in the read model`,
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
        items: {
            type: 'array',
            contains: {
                type: 'ItemRead',
            },
        },
    },
} as const;
