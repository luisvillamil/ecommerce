import React from 'react'
import { 
  Link } from '@tanstack/react-router'
import { useAuth } from '../auth'


function NavBar() {
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
        {auth.isAuthenticated ? (
          <Link
            to={'/dashboard'}
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
      <hr/>
    </>
  )
}

export default NavBar