/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AttributeCreate } from './AttributeCreate';
/**
 * Used by api to create products.
 * extra attributes are appeneded by create_product function in db
 */
export type ProductCreate = {
    name: string;
    description: string;
    category_id?: number;
    attributes?: (Array<AttributeCreate> | null);
};

