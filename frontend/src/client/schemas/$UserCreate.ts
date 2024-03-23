/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $UserCreate = {
    description: `Model to create user.`,
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
        password: {
            type: 'string',
            isRequired: true,
        },
    },
} as const;
