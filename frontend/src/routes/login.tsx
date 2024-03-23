import * as React from 'react'

import {
  createFileRoute,
  getRouteApi,
  useNavigate,
  redirect
} from '@tanstack/react-router'
import { type SubmitHandler, useForm } from "react-hook-form"
import { z } from 'zod'

import {
  type Body_login_get_access_token as AccessToken,
  type ApiError
} from '../client'
import { useAuth } from '../auth'

export const Route = createFileRoute("/login")({
  validateSearch: z.object({
    redirect: z.string().catch('/'),
  }),
  component: LoginComponent,
  beforeLoad: ({context, location}) => {
    if (context.auth.isAuthenticated()) {
      throw redirect({
        to: '/',
        search: {
          redirect: location.href,
        },
      })
    }
  },
})

const routeApi = getRouteApi('/login')

function LoginComponent() {
    const auth = useAuth()
    const navigate = useNavigate()
    const [error, setError] = React.useState<string | null>(null)
    const [show, setShow] = React.useState<boolean>(false)
    const {
      register,
      handleSubmit,
      formState: { errors, isSubmitting },
    } = useForm<AccessToken>({
      mode: "onBlur",
      criteriaMode: "all",
      defaultValues: {
        username: "",
        password: "",
      },
    })

//   const [isSubmitting, setIsSubmitting] = React.useState(false)
//   const [name, setName] = React.useState('')

  const search = routeApi.useSearch()

  const onSubmit: SubmitHandler<AccessToken> = async (data) => {
    try {
      await auth.login(data)
      navigate({ to: search.redirect })
    } catch (err) {
      const errDetail = (err as ApiError).body.detail
      setError(errDetail)
    }
  }

  return (
    <div className="p-2">
      <h3>Login page</h3>
      <p>{error}</p>
      <form className="mt-4" onSubmit={handleSubmit(onSubmit)}>
        <fieldset
          disabled={isSubmitting}
          className="flex flex-col gap-2 max-w-sm"
        >
          <div className="flex gap-2 items-center">
            <label htmlFor="username-input" className="text-sm font-medium">
              Username
            </label>
            <input
              id="username-input"
              type="text"
              {...register("username", {
                pattern: {
                  value: /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i,
                  message: "Invalid email address",
                },
              })}
              // onChange={(e) => setName(e.target.value)}
              className="border border-gray-300 rounded-md p-2 w-full"
              required
            />
          </div>
          <div className="flex gap-2 items-center">
            <label htmlFor="password-input" className="text-sm font-medium">
              Password
            </label>
            <input
              id="password-input"
              {...register("password")}
              type={show ? "text" : "password"}
              // onChange={(e) => setName(e.target.value)}
              className="border border-gray-300 rounded-md p-2 w-full"
              required
            />
          </div>
          <button
            type="submit"
            className="bg-blue-500 text-white py-2 px-4 rounded-md"
          >
            {isSubmitting ? 'Loading...' : 'Login'}
          </button>
        </fieldset>
      </form>
    </div>
  )
}
