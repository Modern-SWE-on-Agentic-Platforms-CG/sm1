import { useState, useCallback } from 'react'
import apiClient from '@/services/api'
import type { AxiosRequestConfig } from 'axios'

interface ApiResponse<T> {
  data: T | null
  error: string | null
  status: 'success' | 'error'
}

export function useApi<T>() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<T | null>(null)

  const request = useCallback(async (config: AxiosRequestConfig): Promise<T | null> => {
    setLoading(true)
    setError(null)
    try {
      const response = await apiClient.request<ApiResponse<T>>(config)
      const body = response.data
      if (body.status === 'error') {
        setError(body.error ?? 'Unknown error')
        return null
      }
      setData(body.data)
      return body.data
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: ApiResponse<T> } })?.response?.data?.error ?? 'Network error'
      setError(msg)
      return null
    } finally {
      setLoading(false)
    }
  }, [])

  return { data, loading, error, request }
}
