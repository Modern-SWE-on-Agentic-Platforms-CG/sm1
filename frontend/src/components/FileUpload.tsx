import { useCallback, useRef, useState } from 'react'
import { Box, Typography, Button, LinearProgress } from '@mui/material'
import CloudUploadIcon from '@mui/icons-material/CloudUpload'

interface Props {
  accept?: string
  maxBytes?: number
  onChange: (file: File) => void
  label?: string
}

const DEFAULT_MAX = 5 * 1024 * 1024 // 5 MB

export default function FileUpload({
  accept = '.xlsx,.xls',
  maxBytes = DEFAULT_MAX,
  onChange,
  label = 'Click or drag a file here to upload',
}: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [error, setError] = useState<string | null>(null)
  const [fileName, setFileName] = useState<string | null>(null)

  const handleFile = useCallback(
    (file: File) => {
      if (file.size > maxBytes) {
        setError(`File too large. Maximum allowed: ${maxBytes / (1024 * 1024)} MB`)
        return
      }
      setError(null)
      setFileName(file.name)
      onChange(file)
    },
    [maxBytes, onChange],
  )

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    if (file) handleFile(file)
  }

  return (
    <Box
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
      sx={{
        border: '2px dashed',
        borderColor: error ? 'error.main' : 'primary.main',
        borderRadius: 2,
        p: 3,
        textAlign: 'center',
        cursor: 'pointer',
        bgcolor: 'action.hover',
      }}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        style={{ display: 'none' }}
        onChange={(e) => {
          const file = e.target.files?.[0]
          if (file) handleFile(file)
        }}
      />
      <CloudUploadIcon color={error ? 'error' : 'primary'} sx={{ fontSize: 40 }} />
      <Typography variant="body1" sx={{ mt: 1 }}>
        {fileName ?? label}
      </Typography>
      {error && (
        <Typography variant="caption" color="error">
          {error}
        </Typography>
      )}
    </Box>
  )
}
