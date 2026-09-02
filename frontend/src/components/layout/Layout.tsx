import { ReactNode } from 'react'
import Sidebar from './Sidebar'
import TopNavbar from './TopNavbar'
import PageHeader from './PageHeader'

export default function Layout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-ink-900 text-ink-100 font-sans">
      <Sidebar />
      <TopNavbar />
      <main className="pl-[14rem] pt-[4.5rem] min-h-screen">
        <PageHeader />
        <div className="px-8 py-8">{children}</div>
      </main>
    </div>
  )
}
