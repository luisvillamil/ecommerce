import * as React from 'react'
import { useQuery } from '@tanstack/react-query'
import { useNavigate } from '@tanstack/react-router'
import {
  LoginService,
  UserService,
  type UserRead,
  type Body_login_get_access_token as AccessToken,
} from './client'

const isLoggedIn = () => {
  return localStorage.getItem('access_token') !== null
}

export interface AuthContext {
  isAuthenticated: boolean
  setUser: (username: string | null) => void
  user: UserRead | null
}
localStorage
const AuthContext = React.createContext<AuthContext | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = React.useState<string | null>(null)
  const isAuthenticated = !!user
  return (
    <AuthContext.Provider value={{ isAuthenticated, user, setUser }}>
      {children}
    </AuthContext.Provider>
  )
}

const useAuth = () => {
  const navigate = useNavigate()
  const { data: user, isLoading } = useQuery<UserRead | null, Error>({
    queryKey: ['users'],
    queryFn: UserService.readUsersMe
  }
  )

  const login = async (data: AccessToken) => {
    const response = await LoginService.getAccessToken({
      formData: data,
    })
    localStorage.setItem('access_token', response.access_token)
    navigate({ to: '/' })
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    navigate({ to: '/login' })
  }

  return { login, logout, user, isLoading }
}

export { isLoggedIn, useAuth }