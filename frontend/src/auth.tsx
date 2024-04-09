import * as React from 'react'
import { queryOptions, useQuery } from '@tanstack/react-query'
import {
  LoginService,
  UserService,
  type UserRead,
  type Body_login_get_access_token as AccessToken,
} from './client'

export interface AuthContext {
  isLoading: boolean
  user: UserRead | null | undefined
  login: (data: AccessToken) =>Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = React.createContext<AuthContext | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {

  const isAuthenticated = !!localStorage.getItem('access_token')

  const { data: user, isLoading, isError, error } = useQuery<UserRead | null, Error>({
    queryKey: ['users'],
    queryFn: UserService.readUsersMe
  })

  if (isError) {
    console.log("error: ", error);
  }
  

  const login = async (data: AccessToken) => {
    const response = await LoginService.getAccessToken({
      formData: data,
    })
    localStorage.setItem('access_token', response.access_token)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
  }

  return (
    <AuthContext.Provider value={{ 
      isLoading, user, login, logout, isAuthenticated}}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = React.useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  // console.log(context)
  return context
}
