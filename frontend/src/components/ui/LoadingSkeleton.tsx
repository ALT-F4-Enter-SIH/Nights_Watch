import { motion } from 'framer-motion'

export default function LoadingSkeleton() {
  return (
    <div className="space-y-4">
      {Array.from({ length: 4 }).map((_, i) => (
        <motion.div
          key={i}
          animate={{ opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.15 }}
          className="h-16 rounded-xl"
          style={{
            background: 'linear-gradient(90deg, #0f1218 40%, #161a28 60%, #0f1218)',
            backgroundSize: '200% 100%',
          }}
        />
      ))}
    </div>
  )
}
