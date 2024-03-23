/* generated using openapi-typescript-codegen -- do no edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Body_login_get_access_token } from '../models/Body_login_get_access_token';
import type { Token } from '../models/Token';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class LoginService {
    /**
     * Get Access Token
     * @returns Token Successful Response
     * @throws ApiError
     */
    public static getAccessToken({
        formData,
    }: {
        formData: Body_login_get_access_token,
    }): CancelablePromise<Token> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/token',
            formData: formData,
            mediaType: 'application/x-www-form-urlencoded',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Read Sub
     * @returns any Successful Response
     * @throws ApiError
     */
    public static readSub(): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/ping',
        });
    }
}
