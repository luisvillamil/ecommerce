/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $ProductRead = {
    description: `Product Read model`,
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
    },
} as const;
