/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserRead = {
    description: `Model to read user`,
    properties: {
        username: {
            type: 'string',
            isRequired: true,
        },
        email: {
            type: 'string',
            isRequired: true,
        },
        full_name: {
            type: 'any-of',
            contains: [{
                type: 'string',
            }, {
                type: 'null',
            }],
        },
        id: {
            type: 'string',
            isRequired: true,
            format: 'uuid',
        },
    },
} as const;
