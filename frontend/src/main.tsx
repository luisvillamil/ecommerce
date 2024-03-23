import React from 'react'
import ReactDOM from 'react-dom/client'
import {QueryClient, QueryClientProvider} from '@tanstack/react-query'
import { createRouter, RouterProvider } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'
import { AuthProvider, useAuth } from './auth'
import { OpenAPI } from './client'

import './index.css'

OpenAPI.BASE = "http://localhost:8000"
const queryClient =  new QueryClient()

const router = createRouter({
  routeTree,
  defaultPreload: 'intent',
  context: {
    auth: undefined!, // This will be set after we wrap the app in an AuthProvider
  }
})
declare module '@tanstack/react-router' {
  interface Register {
    // This infers the type of our router and registers it across your entire project
    router: typeof router
  }
}

function InnerApp() {
  const auth = useAuth()
  return <RouterProvider router={router} context={{ auth }} />
}

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <InnerApp />
      </AuthProvider>
    </QueryClientProvider>
  )
}

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
