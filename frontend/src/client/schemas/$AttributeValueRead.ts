/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export const $AttributeValueRead = {
    description: `AttributeValue Read Model`,
    properties: {
        value: {
            type: 'string',
            isRequired: true,
        },
        attribute_id: {
            type: 'number',
            isRequired: true,
        },
        id: {
            type: 'number',
            isRequired: true,
        },
        attribute: {
            type: 'AttributeRead',
            isRequired: true,
        },
    },
} as const;
