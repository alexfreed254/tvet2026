import { Routes, Route, Navigate } from 'react-router-dom';
import { useAuthStore } from './store/authStore';
import { LoginPage } from './pages/LoginPage';
import { Dashboard } from './pages/Dashboard';
import { AssessmentsList } from './pages/assessments/AssessmentsList';
import { CreateAssessment } from './pages/assessments/CreateAssessment';
import { AssessmentDetail } from './pages/assessments/AssessmentDetail';
import { SelectTrainee } from './pages/marking/SelectTrainee';
import { ConductAssessment } from './pages/marking/ConductAssessment';
import { VerificationQueue } from './pages/verification/VerificationQueue';
import { MarksheetGenerator } from './pages/marksheets/MarksheetGenerator';
import { TraineesList } from './pages/trainees/TraineesList';
import { AppShell } from './components/layout/AppShell';
import { useAuth } from './hooks/useAuth';

function PrivateRoute({ children }: { children: React.ReactNode }) {
  const { user } = useAuthStore();
  if (!user) return <Navigate to="/login" replace />;
  return <AppShell>{children}</AppShell>;
}

export default function App() {
  const { loading } = useAuth();
  if (loading) return <div className="min-h-screen grid place-items-center text-slate-500">Loading TVET e-ASSESS…</div>;
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
      <Route path="/assessments" element={<PrivateRoute><AssessmentsList /></PrivateRoute>} />
      <Route path="/assessments/new" element={<PrivateRoute><CreateAssessment /></PrivateRoute>} />
      <Route path="/assessments/:id" element={<PrivateRoute><AssessmentDetail /></PrivateRoute>} />
      <Route path="/marking/select" element={<PrivateRoute><SelectTrainee /></PrivateRoute>} />
      <Route path="/marking/:sessionId" element={<PrivateRoute><ConductAssessment /></PrivateRoute>} />
      <Route path="/verification" element={<PrivateRoute><VerificationQueue /></PrivateRoute>} />
      <Route path="/marksheets" element={<PrivateRoute><MarksheetGenerator /></PrivateRoute>} />
      <Route path="/trainees" element={<PrivateRoute><TraineesList /></PrivateRoute>} />
    </Routes>
  );
}
