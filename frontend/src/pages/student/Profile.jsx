import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Box,
  Alert,
  Chip,
  Input,
} from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import Layout from '../../components/Layout';
import { getStudentProfile, updateStudentProfile, uploadResume } from '../../services/api';

function Profile({ toggleTheme, mode }) {
  const [profile, setProfile] = useState(null);
  const [formData, setFormData] = useState({});
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await getStudentProfile();
      setProfile(response.data);
      setFormData({
        name: response.data.name,
        college: response.data.college,
        year: response.data.year,
        branch: response.data.branch,
        section: response.data.section || '',
        target_role: response.data.target_role,
        available_hours: response.data.available_hours,
        skills: response.data.skills.join(', '),
      });
    } catch (error) {
      setError('Error fetching profile');
    }
  };

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');
    setError('');

    try {
      const data = {
        ...formData,
        skills: formData.skills.split(',').map(s => s.trim()).filter(s => s),
      };
      await updateStudentProfile(data);
      setMessage('Profile updated successfully!');
      fetchProfile();
    } catch (err) {
      setError('Error updating profile');
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setLoading(true);
    setMessage('');
    setError('');

    try {
      const response = await uploadResume(file);
      setMessage('Resume uploaded and parsed successfully!');
      
      // Update skills if extracted
      if (response.data.extracted_skills.length > 0) {
        setFormData({
          ...formData,
          skills: response.data.extracted_skills.join(', '),
        });
      }
    } catch (err) {
      setError('Error uploading resume');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Typography variant="h4" gutterBottom>
        My Profile
      </Typography>

      {message && <Alert severity="success" sx={{ mb: 2 }}>{message}</Alert>}
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Upload Resume
          </Typography>
          <Box sx={{ mt: 2 }}>
            <label htmlFor="resume-upload">
              <Input
                id="resume-upload"
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                sx={{ display: 'none' }}
              />
              <Button
                variant="contained"
                component="span"
                startIcon={<CloudUpload />}
                disabled={loading}
              >
                Upload Resume (PDF)
              </Button>
            </label>
          </Box>
        </CardContent>
      </Card>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Profile Information
          </Typography>
          <form onSubmit={handleSubmit}>
            <TextField
              fullWidth
              label="Name"
              name="name"
              value={formData.name || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="College"
              name="college"
              value={formData.college || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Year"
              name="year"
              type="number"
              value={formData.year || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Branch"
              name="branch"
              value={formData.branch || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Section"
              name="section"
              value={formData.section || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Target Role"
              name="target_role"
              value={formData.target_role || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Available Hours per Week"
              name="available_hours"
              type="number"
              value={formData.available_hours || ''}
              onChange={handleChange}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Skills (comma separated)"
              name="skills"
              value={formData.skills || ''}
              onChange={handleChange}
              margin="normal"
              helperText="e.g., Python, React, Machine Learning"
            />
            <Button
              type="submit"
              variant="contained"
              size="large"
              sx={{ mt: 3 }}
              disabled={loading}
            >
              {loading ? 'Updating...' : 'Update Profile'}
            </Button>
          </form>
        </CardContent>
      </Card>

      {profile && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Referral Code
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Share this code with friends to earn bonus XP!
            </Typography>
            <Chip label={profile.referral_code} color="primary" sx={{ mt: 1 }} />
          </CardContent>
        </Card>
      )}
    </Layout>
  );
}

export default Profile;
