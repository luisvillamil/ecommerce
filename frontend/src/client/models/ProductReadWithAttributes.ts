/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { AttributeRead } from './AttributeRead';
import type { Image } from './Image';
/**
 * Inherits from CategoryRead, used to display products from category
 */
export type ProductReadWithAttributes = {
    name: string;
    description: string;
    category_id?: number;
    id: number;
    images: Array<Image>;
    attributes?: (Array<AttributeRead> | null);
};

