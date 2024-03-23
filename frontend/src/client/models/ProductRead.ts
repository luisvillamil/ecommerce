/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Image } from './Image';
/**
 * Product Read model
 */
export type ProductRead = {
    name: string;
    description: string;
    category_id?: number;
    id: number;
    images: Array<Image>;
};

