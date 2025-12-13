export type SoutenanceStatus = 'pending' | 'accepted' | 'refused'

export type Domain = 'Web' | 'AI' | 'IoT' | 'Mobile' | 'Security' | 'Data Science' | 'Other'

export interface SoutenanceRequest {
  id: string
  title: string
  domain: Domain
  status: SoutenanceStatus
  pdfUrl?: string
  summary?: string
  similarityScore?: number
  createdAt: string
  updatedAt?: string
  scheduledDate?: string
  scheduledTime?: string
  jury?: string[]
}

export interface RequestFormData {
  title: string
  domain: Domain
  pdfFile: File | null
}

