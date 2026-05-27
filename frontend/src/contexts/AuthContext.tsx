import React, { createContext, useContext, useReducer, ReactNode } from 'react'

export interface Employee {
  emp_id: number
  emp_name: string
  email_id: string
  bu: string | null
  roles: string[]
}

interface AuthState {
  token: string | null
  employee: Employee | null
  activeRole: string | null
}

type AuthAction =
  | { type: 'LOGIN'; token: string; employee: Employee }
  | { type: 'LOGOUT' }
  | { type: 'SET_ACTIVE_ROLE'; role: string }

function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case 'LOGIN':
      return { token: action.token, employee: action.employee, activeRole: null }
    case 'LOGOUT':
      return { token: null, employee: null, activeRole: null }
    case 'SET_ACTIVE_ROLE':
      return { ...state, activeRole: action.role }
    default:
      return state
  }
}

interface AuthContextValue extends AuthState {
  login: (token: string, employee: Employee) => void
  logout: () => void
  setActiveRole: (role: string) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const storedToken = localStorage.getItem('access_token')
  const storedEmployee = localStorage.getItem('employee')

  const [state, dispatch] = useReducer(authReducer, {
    token: storedToken,
    employee: storedEmployee ? JSON.parse(storedEmployee) : null,
    activeRole: localStorage.getItem('active_role'),
  })

  const login = (token: string, employee: Employee) => {
    // Local-dev only: store token in localStorage
    // Production: use httpOnly cookie set by backend
    localStorage.setItem('access_token', token)
    localStorage.setItem('employee', JSON.stringify(employee))
    dispatch({ type: 'LOGIN', token, employee })
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('employee')
    localStorage.removeItem('active_role')
    dispatch({ type: 'LOGOUT' })
  }

  const setActiveRole = (role: string) => {
    localStorage.setItem('active_role', role)
    dispatch({ type: 'SET_ACTIVE_ROLE', role })
  }

  return (
    <AuthContext.Provider value={{ ...state, login, logout, setActiveRole }}>
      {children}
    </AuthContext.Provider>
  )
}

export default AuthContext
