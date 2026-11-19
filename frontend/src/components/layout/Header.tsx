import { useAuthStore } from '../../store/authStore';
import { LogOut, User } from 'lucide-react';

export function Header() {
  const { user, logout } = useAuthStore();
  return (
    <header className="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
      <div>
        <h2 className="text-lg font-semibold text-gray-900">TVET e-ASSESS</h2>
        <p className="text-sm text-gray-500">Assess Digitally. Verify Competence. Preserve Evidence.</p>
      </div>
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2">
          <User className="h-5 w-5 text-gray-500" />
          <div className="text-sm">
            <p className="font-medium text-gray-900">{user ? `${user.first_name} ${user.last_name}` : 'Guest'}</p>
            <p className="text-xs text-gray-500">{user?.role || ''}</p>
          </div>
        </div>
        <button onClick={logout} className="p-2 rounded-md hover:bg-gray-100" title="Logout">
          <LogOut className="h-5 w-5 text-gray-600" />
        </button>
      </div>
    </header>
  );
}
