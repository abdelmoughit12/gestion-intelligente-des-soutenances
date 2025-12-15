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




// Types basés sur l'entité Notification (Tâche 4.4)
export interface Notification {
    id: number;
    message: string;
    type_action: 'ASSIGNMENT' | 'ACCEPTANCE' | 'REFUSAL' | 'DATE_SCHEDULED';
    date_creation: string;
    est_lue: boolean;
}

export interface AssignedSoutenance {
  id: number
  title: string
  studentName: string
  studentEmail: string
  domain: Domain
  status: 'pending' | 'in_progress' | 'evaluated' | 'scheduled'
  scheduledDate?: string
  scheduledTime?: string
  defendanceDate?: string
  defendanceTime?: string
  reportId: number
  aiSummary?: string
  aiSimilarityScore?: number
  juryRole: 'president' | 'member' | 'secretary' | 'examiner'
  evaluationScore?: number
  evaluationComments?: string
  evaluationDate?: string
  evaluatedByProfessor?: string
}

export interface ProfessorStats {
  assignedCount: number
  evaluatedCount: number
  pendingCount: number
  scheduledCount: number
}

export interface ProfessorNotification extends Notification {
  defensesId?: number
  studentName?: string
}

// Évaluation des soutenances
export interface EvaluationSubmission {
  soutenanceId: number
  score: number
  comments: string
  submittedAt: string
  submittedBy: string
}

export interface EvaluationData {
  score: number
  comments: string
}