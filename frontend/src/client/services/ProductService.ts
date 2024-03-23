/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_product_post_image } from '../models/Body_product_post_image';
import type { ProductCreate } from '../models/ProductCreate';
import type { ProductReadWithAttributes } from '../models/ProductReadWithAttributes';
import type { ProductReadWithItems } from '../models/ProductReadWithItems';
import type { ProductUpdate } from '../models/ProductUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ProductService {
    /**
     * Post Product
     * creates category from defined schema. Admin only
     * @returns ProductReadWithAttributes Successful Response
     * @throws ApiError
     */
    public static postProduct({
        requestBody,
    }: {
        requestBody: ProductCreate,
    }): CancelablePromise<ProductReadWithAttributes> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/product',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Product
     * creates category from defined schema. Admin only
     * @returns ProductReadWithAttributes Successful Response
     * @throws ApiError
     */
    public static getProduct({
        id,
    }: {
        id: number,
    }): CancelablePromise<ProductReadWithAttributes> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Put Product
     * creates category from defined schema. Admin only
     * @returns ProductReadWithAttributes Successful Response
     * @throws ApiError
     */
    public static putProduct({
        id,
        requestBody,
    }: {
        id: string,
        requestBody: ProductUpdate,
    }): CancelablePromise<ProductReadWithAttributes> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/product',
            query: {
                '_id': id,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Product
     * creates category from defined schema. Admin only
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteProduct({
        id,
    }: {
        id: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/product',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Post Image
     * Uploads image, adds it directly to product
     * @returns any Successful Response
     * @throws ApiError
     */
    public static postImage({
        id,
        formData,
    }: {
        id: number,
        formData: Body_product_post_image,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/product/image',
            query: {
                '_id': id,
            },
            formData: formData,
            mediaType: 'multipart/form-data',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Product By Name
     * creates category from defined schema. Admin only
     * @returns ProductReadWithAttributes Successful Response
     * @throws ApiError
     */
    public static getProductByName({
        name,
    }: {
        name: string,
    }): CancelablePromise<ProductReadWithAttributes> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product/name',
            query: {
                'name': name,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Product List
     * Gets list of products with items
     *
     * Args:
     * offset (int, optional): page offset. Defaults to 0.
     * limit (int, optional): number of products per page. Defaults to Query(default=100, le=100).
     * @returns ProductReadWithItems Successful Response
     * @throws ApiError
     */
    public static getProductList({
        offset,
        limit = 100,
    }: {
        offset?: number,
        limit?: number,
    }): CancelablePromise<Array<ProductReadWithItems>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/product/list',
            query: {
                'offset': offset,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
