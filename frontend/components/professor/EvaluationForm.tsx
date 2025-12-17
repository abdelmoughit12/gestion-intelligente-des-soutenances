'use client'

import { useState } from 'react'
import { AlertCircle, CheckCircle, Loader } from 'lucide-react'
import { submitEvaluation } from '@/services/api'

interface Props {
  soutenanceId: number
  studentName: string
  onSubmitSuccess: () => void
  onCancel: () => void
  initialData?: {
    score?: number
    comments?: string
  }
}

export default function EvaluationForm({
  soutenanceId,
  studentName,
  onSubmitSuccess,
  onCancel,
  initialData = {},
}: Props) {
  const [score, setScore] = useState<number>(initialData.score || 0)
  const [comments, setComments] = useState<string>(initialData.comments || '')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)
  const [showConfirm, setShowConfirm] = useState(false)

  const isEditMode = initialData.score !== undefined

  // Validation
  const isValid = score >= 0 && score <= 20 
  const scorePercentage = (score / 20) * 100

  const getScoreColor = (value: number) => {
    if (value < 10) return 'text-red-600'
    if (value < 14) return 'text-yellow-600'
    if (value < 16) return 'text-blue-600'
    return 'text-green-600'
  }

  const handleSubmit = async () => {
    if (!isValid) {
      setError('Veuillez vérifier que la note est entre 0-20 et les commentaires contiennent au moins 10 caractères')
      return
    }

    setLoading(true)
    setError(null)

    try {
      // Appeler l'API backend pour soumettre l'évaluation
      await submitEvaluation(soutenanceId, { score, comments })

      setSuccess(true)
      setTimeout(() => {
        onSubmitSuccess()
      }, 1500)
    } catch (err: any) {
      setError(err.message || 'Erreur lors de la soumission')
    } finally {
      setLoading(false)
    }
  }

  if (success) {
    return (
      <div className="bg-green-50 border border-green-200 rounded-lg p-6 text-center">
        <CheckCircle className="h-12 w-12 text-green-600 mx-auto mb-3" />
        <h3 className="text-lg font-semibold text-green-900 mb-2">Évaluation Soumise</h3>
        <p className="text-green-700 text-sm">
          L évaluation pour {studentName} a été sauvegardée avec succès.
        </p>
      </div>
    )
  }

  return (
    <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 space-y-4">
      <div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">{isEditMode ? 'Modifier l\'évaluation' : 'Évaluer la Soutenance'}</h3>
        <p className="text-sm text-gray-600">Étudiant: {studentName}</p>
      </div>

      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 flex gap-3">
          <AlertCircle className="h-5 w-5 text-red-600 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Note Finale */}
      <div>
        <label htmlFor="score" className="block text-sm font-medium text-gray-700 mb-2">
          Note Finale (0-20)
        </label>
        <div className="flex items-center gap-4">
          <input
            id="score"
            type="range"
            min="0"
            max="20"
            step="0.5"
            value={score}
            onChange={(e) => setScore(parseFloat(e.target.value))}
            disabled={loading}
            className="flex-1 h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer"
          />
          <span className={`text-2xl font-bold min-w-fit ${getScoreColor(score)}`}>
            {score.toFixed(1)}/20
          </span>
        </div>
        <div className="mt-2 h-1 bg-gray-200 rounded-full overflow-hidden">
          <div
            className={`h-full transition-all ${
              score < 10
                ? 'bg-red-500'
                : score < 14
                ? 'bg-yellow-500'
                : score < 16
                ? 'bg-blue-500'
                : 'bg-green-500'
            }`}
            style={{ width: `${scorePercentage}%` }}
          />
        </div>
        <div className="mt-2 flex justify-between text-xs text-gray-500">
          <span>Échec (0-10)</span>
          <span>Bien (14-16)</span>
          <span>Excellent (16-20)</span>
        </div>
      </div>

      {/* Commentaires */}
      <div>
        <label htmlFor="comments" className="block text-sm font-medium text-gray-700 mb-2">
          Commentaires Détaillés

        </label>
        <textarea
          id="comments"
          value={comments}
          onChange={(e) => setComments(e.target.value)}
          disabled={loading}
          placeholder="Décrivez les points forts et les points à améliorer..."
          rows={4}
          className="w-full px-3 py-2 border border-gray-900 text-black bg-white rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-600 disabled:bg-gray-100"
        />
      
      </div>

      {/* Boutons d'action */}
      {!showConfirm ? (
        <div className="flex gap-3 pt-4">
          <button
            onClick={() => setShowConfirm(true)}
            disabled={!isValid || loading}
            className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition font-medium"
          >
            {loading ? (
              <>
                <Loader className="h-4 w-4 inline mr-2 animate-spin" />
                Envoi en cours...
              </>
            ) : (
              isEditMode ? 'Mettre à jour' : 'Soumettre l\'Évaluation'
            )}
          </button>
          <button
            onClick={onCancel}
            disabled={loading}
            className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 disabled:bg-gray-100 transition"
          >
            Annuler
          </button>
        </div>
      ) : (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-4">
          <div>
            <h4 className="font-semibold text-gray-900 mb-2">Confirmer l Évaluation?</h4>
            <p className="text-sm text-gray-700 mb-2">
              <strong>Étudiant:</strong> {studentName}
            </p>
            <p className="text-sm text-gray-700 mb-2">
              <strong>Note:</strong>{' '}
              <span className={`font-bold ${getScoreColor(score)}`}>{score.toFixed(1)}/20</span>
            </p>
            <p className="text-sm text-gray-700">
              <strong>Commentaires:</strong> {comments.substring(0, 50)}
              {comments.length > 50 ? '...' : ''}
            </p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleSubmit}
              disabled={loading}
              className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 transition font-medium"
            >
              {loading ? (
                <>
                  <Loader className="h-4 w-4 inline mr-2 animate-spin" />
                  Envoi...
                </>
              ) : (
                'Confirmer'
              )}
            </button>
            <button
              onClick={() => setShowConfirm(false)}
              disabled={loading}
              className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-100 disabled:bg-gray-100 transition"
            >
              Modifier
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
