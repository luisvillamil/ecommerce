import { Outlet, createFileRoute, redirect } from '@tanstack/react-router'
import { useAuth } from '../auth'

// export const Route = createFileRoute('/_admin')({
//   beforeLoad: async ({context, location}) => {
//     console.log("_admin beforeload admin:", context.auth)
//     if (!context.auth.isAuthenticated) {
//       throw redirect({
//         to: '/login',
//         search: {
//           redirect: location.href,
//         },
//         replace: true
//       })
//     }
//   },
//   component: () => {
//     const {isLoading} = useAuth()
  
//     return (
//       <>
//         {isLoading ? (
//           <h1>Loading</h1>
//         ) : (
//           <Outlet />
//         )}
//         <p>menu</p>
//       </>
//     )
//   },
// })

export const Route = createFileRoute('/_admin')({
  // Before loading, authenticate the user via our auth context
  // This will also happen during prefetching (e.g. hovering over links, etc)
  beforeLoad: ({ context, location }) => {
    // If the user is logged out, redirect them to the login page
    if (!context.auth.isAuthenticated) {
      throw redirect({
        to: '/login',
        search: {
          // Use the current location to power a redirect after login
          // (Do not use `router.state.resolvedLocation` as it can
          // potentially lag behind the actual current location)
          redirect: location.href,
        },
      })
    }

    // Otherwise, return the user in context
    return {
      auth: context.auth,
    }
  },
})
