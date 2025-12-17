'use client'

import { useCallback, useState } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, FileText, X, CheckCircle } from 'lucide-react'

interface PDFUploadProps {
  onFileSelect: (file: File) => void
  selectedFile: File | null
}

export default function PDFUpload({ onFileSelect, selectedFile }: PDFUploadProps) {
  const [error, setError] = useState<string | null>(null)

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      setError(null)
      const file = acceptedFiles[0]

      if (file) {
        // Validate file type
        if (file.type !== 'application/pdf') {
          setError('Please upload a PDF file only')
          return
        }

        // Validate file size (max 10MB)
        const maxSize = 10 * 1024 * 1024 // 10MB
        if (file.size > maxSize) {
          setError('File size must be less than 10MB')
          return
        }

        onFileSelect(file)
      }
    },
    [onFileSelect]
  )

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
  })

  const handleRemove = (e: React.MouseEvent) => {
    e.stopPropagation()
    onFileSelect(null as any)
    setError(null)
  }

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes'
    const k = 1024
    const sizes = ['Bytes', 'KB', 'MB', 'GB']
    const i = Math.floor(Math.log(bytes) / Math.log(k))
    return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i]
  }

  return (
    <div>
      {selectedFile ? (
        <div className="border-2 border-green-500 rounded-lg p-4 bg-green-50">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <CheckCircle className="h-5 w-5 text-green-600" />
              <div>
                <div className="flex items-center space-x-2">
                  <FileText className="h-4 w-4 text-gray-600" />
                  <span className="font-medium text-gray-900">{selectedFile.name}</span>
                </div>
                <p className="text-sm text-gray-500 mt-1">
                  {formatFileSize(selectedFile.size)}
                </p>
              </div>
            </div>
            <button
              onClick={handleRemove}
              className="text-red-600 hover:text-red-800 transition-colors"
            >
              <X className="h-5 w-5" />
            </button>
          </div>
        </div>
      ) : (
        <div
          {...getRootProps()}
          className={`
            border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
            ${
              isDragActive
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-300 hover:border-primary-400 hover:bg-gray-50'
            }
          `}
        >
          <input {...getInputProps()} />
          <div className="flex flex-col items-center space-y-4">
            <Upload
              className={`h-12 w-12 ${isDragActive ? 'text-primary-600' : 'text-gray-400'}`}
            />
            <div>
              <p className="text-sm font-medium text-gray-700">
                {isDragActive ? (
                  <span className="text-primary-600">Drop the PDF here</span>
                ) : (
                  <>
                    <span className="text-primary-600">Click to upload</span> or drag and drop
                  </>
                )}
              </p>
              <p className="text-xs text-gray-500 mt-1">PDF only (Max. 10MB)</p>
            </div>
          </div>
        </div>
      )}

      {error && (
        <p className="mt-2 text-sm text-red-600 flex items-center space-x-1">
          <X className="h-4 w-4" />
          <span>{error}</span>
        </p>
      )}
    </div>
  )
}

