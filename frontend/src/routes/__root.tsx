import React, { Suspense } from 'react'
import { 
  createRootRouteWithContext,
  ErrorComponent,
  Outlet } from '@tanstack/react-router'
import { ReactQueryDevtools } from '@tanstack/react-query-devtools'
import { type AuthContext } from '../auth'
// import NavBar from '../components/NavBar'

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
  ({ component: RootComponent,
    errorComponent: ({error}) => {
      return <ErrorComponent error={error} />
    }})


function RootComponent() {
  return (
    <>
      {/* <NavBar/> */}
      <Outlet />
      <Suspense>
        <ReactQueryDevtools buttonPosition="top-right" />
        <TanStackRouteDevtools position='bottom-right' />
      </Suspense>
    </>
  )
}
