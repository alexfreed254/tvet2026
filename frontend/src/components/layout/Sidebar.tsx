import { NavLink } from 'react-router-dom';
import { LayoutDashboard, FileText, ClipboardCheck, CheckSquare, Table, Users } from 'lucide-react';

const links = [
  { to: '/', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/assessments', label: 'Assessments', icon: FileText },
  { to: '/marking/select', label: 'Conduct Assessment', icon: ClipboardCheck },
  { to: '/verification', label: 'Verification', icon: CheckSquare },
  { to: '/marksheets', label: 'Marksheets', icon: Table },
  { to: '/trainees', label: 'Trainees', icon: Users },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-slate-900 text-white flex flex-col">
      <div className="p-6 border-b border-slate-700">
        <h1 className="text-xl font-bold">TVET e-ASSESS</h1>
        <p className="text-xs text-slate-400 mt-1">Digital Assessment Platform</p>
      </div>
      <nav className="flex-1 p-4 space-y-1">
        {links.map((link) => (
          <NavLink key={link.to} to={link.to} className={({ isActive }) => `flex items-center gap-3 px-3 py-2 rounded-md text-sm transition-colors ${isActive ? 'bg-slate-800 text-white' : 'text-slate-300 hover:bg-slate-800 hover:text-white'}`}>
            <link.icon className="h-5 w-5" />
            {link.label}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-slate-700 text-xs text-slate-400">
        © 2026 TVET e-ASSESS
      </div>
    </aside>
  );
}
