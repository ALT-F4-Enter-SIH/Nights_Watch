import { motion, useInView } from 'framer-motion'
import { useRef, useState, useEffect } from 'react'

function AnimatedNumber({ value, duration = 1.2, decimals = 0 }: { value: number; duration?: number; decimals?: number }) {
  const ref = useRef(null)
  const inView = useInView(ref, { once: true })
  const [display, setDisplay] = useState(0)
  useEffect(() => {
    if (!inView) return
    let start = 0
    const startTime = performance.now()
    const animate = (now: number) => {
      const progress = Math.min((now - startTime) / (duration * 1000), 1)
      const eased = 1 - Math.pow(1 - progress, 3)
      setDisplay(start + (value - start) * eased)
      if (progress < 1) requestAnimationFrame(animate)
    }
    requestAnimationFrame(animate)
  }, [inView, value, duration])
  return (
    <span ref={ref} className="font-mono tracking-tight tabular-nums">
      {decimals ? display.toFixed(decimals) : Math.round(display).toLocaleString()}
    </span>
  )
}

export default AnimatedNumber
