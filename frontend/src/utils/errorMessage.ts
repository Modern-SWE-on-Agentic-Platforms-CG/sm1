export function getApiErrorMessage(error: unknown, fallback = 'Request failed'): string {
  const err = error as {
    message?: string
    response?: {
      data?: {
        error?: string
        detail?: string | Array<{ loc?: Array<string | number>; msg?: string }>
        message?: string
      }
      status?: number
    }
  }

  const data = err?.response?.data

  if (typeof data?.error === 'string' && data.error.trim()) {
    return data.error
  }

  if (typeof data?.message === 'string' && data.message.trim()) {
    return data.message
  }

  if (typeof data?.detail === 'string' && data.detail.trim()) {
    return data.detail
  }

  if (Array.isArray(data?.detail) && data.detail.length > 0) {
    const first = data.detail[0]
    if (typeof first?.msg === 'string' && first.msg.trim()) {
      const loc = Array.isArray(first.loc) ? first.loc.join('.') : ''
      return loc ? `${loc}: ${first.msg}` : first.msg
    }
  }

  if (typeof err?.message === 'string' && err.message.trim()) {
    return err.message
  }

  return fallback
}