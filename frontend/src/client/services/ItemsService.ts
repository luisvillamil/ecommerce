/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemCreate } from '../models/ItemCreate';
import type { ItemRead } from '../models/ItemRead';
import type { ItemUpdate } from '../models/ItemUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemsService {
    /**
     * Get Item List
     * gets item list
     * @returns ItemRead Successful Response
     * @throws ApiError
     */
    public static getItemList({
        offset,
        limit = 100,
    }: {
        offset?: number,
        limit?: number,
    }): CancelablePromise<Array<ItemRead>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/item/list',
            query: {
                'offset': offset,
                'limit': limit,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Post Item
     * Creates item
     * @returns ItemRead Successful Response
     * @throws ApiError
     */
    public static postItem({
        requestBody,
    }: {
        requestBody: ItemCreate,
    }): CancelablePromise<ItemRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/item',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Item
     * Gets item by specified _id
     * @returns ItemRead Successful Response
     * @throws ApiError
     */
    public static getItem({
        id,
    }: {
        id: number,
    }): CancelablePromise<ItemRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/item',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Item
     * Updates item specified by id
     * @returns ItemRead Successful Response
     * @throws ApiError
     */
    public static updateItem({
        id,
        requestBody,
    }: {
        id: number,
        requestBody: ItemUpdate,
    }): CancelablePromise<ItemRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/item',
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
     * Delete Item
     * Deletes item specified by id
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteItem({
        id,
    }: {
        id: number,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/item',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
