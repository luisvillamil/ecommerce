/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CategoryCreate } from '../models/CategoryCreate';
import type { CategoryRead } from '../models/CategoryRead';
import type { CategoryReadWithProducts } from '../models/CategoryReadWithProducts';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CategoryService {
    /**
     * Post Category
     * creates category from defined schema. Admin only
     * @returns CategoryRead Successful Response
     * @throws ApiError
     */
    public static postCategory({
        requestBody,
    }: {
        requestBody: CategoryCreate,
    }): CancelablePromise<CategoryRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/category',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Category Endpoint
     * Gets category by _id, should return with products associated to category
     *
     * Args:
     * _id (int): id of category
     *
     * Raises:
     * HTTPException: if category not found
     * @returns CategoryReadWithProducts Successful Response
     * @throws ApiError
     */
    public static getCategoryEndpoint({
        id,
    }: {
        id: number,
    }): CancelablePromise<CategoryReadWithProducts> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/category',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Category Endpoint
     * Deletes category by _id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteCategoryEndpoint({
        id,
    }: {
        id: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/category',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Category List Endpoint
     * Returns list of categories
     * @returns CategoryRead Successful Response
     * @throws ApiError
     */
    public static getCategoryListEndpoint({
        offset,
        limit = 100,
    }: {
        offset?: number,
        limit?: number,
    }): CancelablePromise<Array<CategoryRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/category/list',
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
