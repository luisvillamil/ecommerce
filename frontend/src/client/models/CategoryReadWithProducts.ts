/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ProductRead } from './ProductRead';
/**
 * Inherits from CategoryRead, used to display products from category
 */
export type CategoryReadWithProducts = {
    name: string;
    id: number;
    products?: (Array<ProductRead> | null);
};

