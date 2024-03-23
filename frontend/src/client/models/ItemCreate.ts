/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AttributeValueCreate } from './AttributeValueCreate';
/**
 * For creating items, include a list of AttributeValueCreate instances
 */
export type ItemCreate = {
    name: string;
    description?: string;
    stock_quantity: number;
    sku?: (string | null);
    product_id: number;
    price: number;
    attribute_values?: (Array<AttributeValueCreate> | null);
};

