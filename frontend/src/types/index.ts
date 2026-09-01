export interface Identity {
  id: string
  username: string
  aliases: string[]
  email?: string
  pgp_fingerprint?: string
  crypto_wallets: string[]
  platform?: string
  bio?: string
  writing_samples: string[]
  posting_hours: number[]
  categories: string[]
  metadata: Record<string, unknown>
  source_id?: string
  created_at: string
  updated_at: string
}

export interface Relation {
  id: string
  source_identity_id: string
  target_identity_id: string
  correlation_type: string
  confidence_score: number
  evidence: Record<string, unknown>
  explanation?: string
  created_at: string
}

export interface AnalysisRun {
  id: string
  run_type: string
  identities_processed: number
  relations_found: number
  duration_seconds: number
  status: string
  created_at: string
  completed_at?: string
}

export interface AnalyticsOverview {
  identities: number
  relations: number
  avg_confidence: number
  sources: number
}
