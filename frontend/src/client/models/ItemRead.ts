/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AttributeValueRead } from './AttributeValueRead';
import type { ProductRead } from './ProductRead';
/**
 * Reading items back, include detailed attribute value information
 */
export type ItemRead = {
    name: string;
    description?: string;
    stock_quantity: number;
    sku?: (string | null);
    product_id: number;
    price: number;
    id: number;
    product: ProductRead;
    attribute_values?: Array<AttributeValueRead>;
};

