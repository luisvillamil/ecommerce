/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { UserCreate } from '../models/UserCreate';
import type { UserRead } from '../models/UserRead';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class UserService {
    /**
     * Create User Endpoint
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static createUserEndpoint({
        requestBody,
    }: {
        requestBody: UserCreate,
    }): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/user',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get User Endpoint
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static getUserEndpoint({
        id,
    }: {
        id: string,
    }): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/user',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update User Endpoint
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static updateUserEndpoint({
        id,
        kwargs,
    }: {
        id: string,
        kwargs: any,
    }): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/user',
            query: {
                '_id': id,
                'kwargs': kwargs,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete User Endpoint
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteUserEndpoint({
        id,
    }: {
        id: string,
    }): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/user',
            query: {
                '_id': id,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Read Users Me
     * @returns UserRead Successful Response
     * @throws ApiError
     */
    public static readUsersMe(): CancelablePromise<UserRead> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/users/me/',
        });
    }
}
