import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';
import { useState, useEffect } from 'react';
import Login from './pages/Login';
import Register from './pages/Register';
import StudentDashboard from './pages/student/Dashboard';
import StudentProfile from './pages/student/Profile';
import StudentPlan from './pages/student/Plan';
import StudentLeaderboard from './pages/student/Leaderboard';
import StudentAssessment from './pages/student/Assessment';
import HRDashboard from './pages/hr/Dashboard';
import HRTalentList from './pages/hr/TalentList';
import HRAnalytics from './pages/hr/Analytics';

function App() {
  const [mode, setMode] = useState('light');
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
  }, []);

  const theme = createTheme({
    palette: {
      mode,
      primary: {
        main: '#1976d2',
      },
      secondary: {
        main: '#dc004e',
      },
    },
    typography: {
      fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
    },
  });

  const toggleTheme = () => {
    setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
  };

  const ProtectedRoute = ({ children, role }) => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    
    if (!token || !userData) {
      return <Navigate to="/login" />;
    }

    const user = JSON.parse(userData);
    if (role && user.role !== role) {
      return <Navigate to="/login" />;
    }

    return children;
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/login" element={<Login setUser={setUser} />} />
          <Route path="/register" element={<Register />} />
          
          {/* Student Routes */}
          <Route
            path="/student/dashboard"
            element={
              <ProtectedRoute role="STUDENT">
                <StudentDashboard toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/profile"
            element={
              <ProtectedRoute role="STUDENT">
                <StudentProfile toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/plan"
            element={
              <ProtectedRoute role="STUDENT">
                <StudentPlan toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/leaderboard"
            element={
              <ProtectedRoute role="STUDENT">
                <StudentLeaderboard toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/student/assessment"
            element={
              <ProtectedRoute role="STUDENT">
                <StudentAssessment toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />

          {/* HR Routes */}
          <Route
            path="/hr/dashboard"
            element={
              <ProtectedRoute role="HR">
                <HRDashboard toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/hr/talent"
            element={
              <ProtectedRoute role="HR">
                <HRTalentList toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />
          <Route
            path="/hr/analytics"
            element={
              <ProtectedRoute role="HR">
                <HRAnalytics toggleTheme={toggleTheme} mode={mode} />
              </ProtectedRoute>
            }
          />

          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;
