import { useState, useEffect } from 'react';
import { useNavigate, Link, useSearchParams } from 'react-router-dom';
import {
  Container,
  Box,
  Paper,
  TextField,
  Button,
  Typography,
  Alert,
  ToggleButtonGroup,
  ToggleButton,
  Chip,
} from '@mui/material';
import { register } from '../services/api';

function Register() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const [role, setRole] = useState('STUDENT');
  const [referralCode, setReferralCode] = useState('');
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    name: '',
    college: '',
    year: '',
    branch: '',
    target_role: '',
    company: '',
    designation: '',
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Check for referral code in URL
    const ref = searchParams.get('ref');
    if (ref) {
      setReferralCode(ref);
    }
  }, [searchParams]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleRoleChange = (event, newRole) => {
    if (newRole !== null) {
      setRole(newRole);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const data = { 
        email: formData.email,
        password: formData.password,
        name: formData.name,
        role 
      };
      
      // Add role-specific fields
      if (role === 'STUDENT') {
        data.college = formData.college;
        data.year = parseInt(formData.year);
        data.branch = formData.branch;
        data.target_role = formData.target_role;
        
        // Add referral code if present
        if (referralCode) {
          data.referral_code = referralCode;
        }
      } else {
        data.company = formData.company;
        if (formData.designation) {
          data.designation = formData.designation;
        }
      }
      
      await register(data);
      
      // Show success message about referral bonus
      if (referralCode && role === 'STUDENT') {
        alert('🎉 Registration successful! You earned 25 XP from referral bonus!');
      }
      
      navigate('/login');
    } catch (err) {
      console.error('Registration error:', err);
      setError(err.response?.data?.detail || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Typography variant="h3" component="h1" gutterBottom>
          KaiHire
        </Typography>
        
        <Paper elevation={3} sx={{ p: 4, mt: 3, width: '100%' }}>
          <Typography variant="h5" component="h2" gutterBottom>
            Register
          </Typography>
          
          {referralCode && (
            <Alert severity="success" sx={{ mb: 2 }}>
              🎉 Referral Code Applied: <strong>{referralCode}</strong>
              <br />
              You'll get 25 XP bonus on signup!
            </Alert>
          )}
          
          {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
          
          <Box sx={{ mb: 3, display: 'flex', justifyContent: 'center' }}>
            <ToggleButtonGroup
              value={role}
              exclusive
              onChange={handleRoleChange}
              aria-label="user role"
            >
              <ToggleButton value="STUDENT">Student</ToggleButton>
              <ToggleButton value="HR">HR</ToggleButton>
            </ToggleButtonGroup>
          </Box>
          
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Name"
              name="name"
              value={formData.name}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Email"
              name="email"
              type="email"
              value={formData.email}
              onChange={handleChange}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Password"
              name="password"
              type="password"
              value={formData.password}
              onChange={handleChange}
              margin="normal"
              required
            />
            
            {role === 'STUDENT' ? (
              <>
                <TextField
                  fullWidth
                  label="College"
                  name="college"
                  value={formData.college}
                  onChange={handleChange}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Year"
                  name="year"
                  type="number"
                  value={formData.year}
                  onChange={handleChange}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Branch"
                  name="branch"
                  value={formData.branch}
                  onChange={handleChange}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Target Role (e.g., SDE, ML Engineer)"
                  name="target_role"
                  value={formData.target_role}
                  onChange={handleChange}
                  margin="normal"
                  required
                />
              </>
            ) : (
              <>
                <TextField
                  fullWidth
                  label="Company"
                  name="company"
                  value={formData.company}
                  onChange={handleChange}
                  margin="normal"
                  required
                />
                <TextField
                  fullWidth
                  label="Designation"
                  name="designation"
                  value={formData.designation}
                  onChange={handleChange}
                  margin="normal"
                />
              </>
            )}
            
            <Button
              type="submit"
              fullWidth
              variant="contained"
              size="large"
              sx={{ mt: 3 }}
              disabled={loading}
            >
              {loading ? 'Registering...' : 'Register'}
            </Button>
          </form>
          
          <Box sx={{ mt: 2, textAlign: 'center' }}>
            <Typography variant="body2">
              Already have an account?{' '}
              <Link to="/login" style={{ textDecoration: 'none', color: '#1976d2' }}>
                Login here
              </Link>
            </Typography>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
}

export default Register;
