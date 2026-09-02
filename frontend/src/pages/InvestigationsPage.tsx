import { motion } from 'framer-motion'
import MetricCard from '../components/ui/MetricCard'
import LoadingSkeleton from '../components/ui/LoadingSkeleton'

export default function InvestigationsPage() {
  return (
    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.3 }}>
      <h2 className="text-xl font-bold tracking-tight text-ink-100 mb-4">Investigations</h2>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <MetricCard label="Open" value="3" sub="Active cases" />
        <MetricCard label="In Review" value="2" sub="Pending analysis" />
        <MetricCard label="Critical" value="1" sub="High priority" delta="HIGH" deltaColor="critical" />
      </div>
      <LoadingSkeleton />
    </motion.div>
  )
}
