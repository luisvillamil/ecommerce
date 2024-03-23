import React, { Suspense } from 'react'
import { Link, Outlet, createRootRouteWithContext } from '@tanstack/react-router'
import { useAuth, type AuthContext } from '../auth'

interface MyRouterContext {
  auth: AuthContext
}

const TanStackRouteDevtools = 
  process.env.NODE_ENV === 'prod'
    ? () => null
    : React.lazy(() =>
      import('@tanstack/router-devtools').then((res) => ({
        default: res.TanStackRouterDevtools,
      })),
    )

export const Route = createRootRouteWithContext<MyRouterContext>()
  ({ component: RootComponent,})


function RootComponent() {
  const auth = useAuth()
  return (
    <>
      <div className='p-2 flex gap-2 text-lg'>
        <Link
          to="/"
          activeProps={{
            className: 'font-bold',
          }}
          activeOptions={{ exact: true }}
        >
          Home
        </Link>{' '}
        {auth.isAuthenticated() ? (
          <Link
            to={'/admin/dashboard'}
            activeProps={{
              className: 'font-bold',
            }}
          >
            Dashboard
          </Link>
        ) : (
          <Link
            to={'/login'}
            activeProps={{
              className: 'font-bold',
            }}
            search={{ redirect: '/' }}
          >
            Login
          </Link>
        )}
      </div>
      <Outlet />
      <Suspense>
        <TanStackRouteDevtools position='bottom-right' />
      </Suspense>
    </>
  )
}
