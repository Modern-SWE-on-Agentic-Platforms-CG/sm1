import { BrowserRouter } from 'react-router-dom'
import { AuthProvider } from '@/contexts/AuthContext'
import AppRoutes from '@/routes'
import ApiErrorBoundary from '@/components/ApiErrorBoundary'

export default function App() {
  return (
    <ApiErrorBoundary>
      <AuthProvider>
        <BrowserRouter>
          <AppRoutes />
        </BrowserRouter>
      </AuthProvider>
    </ApiErrorBoundary>
  )
}
