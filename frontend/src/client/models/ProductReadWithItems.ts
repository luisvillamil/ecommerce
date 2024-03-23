/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Image } from './Image';
import type { ItemRead } from './ItemRead';
/**
 * Update the Product models to include items with attributes in the read model
 */
export type ProductReadWithItems = {
    name: string;
    description: string;
    category_id?: number;
    id: number;
    images: Array<Image>;
    items?: Array<ItemRead>;
};

