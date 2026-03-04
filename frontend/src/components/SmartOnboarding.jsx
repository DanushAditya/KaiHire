import { useState } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  MenuItem,
  Chip,
  Stack,
  Stepper,
  Step,
  StepLabel,
  Alert,
  CircularProgress
} from '@mui/material';
import { motion } from 'framer-motion';
import axios from 'axios';

const ROLES = [
  'Software Developer',
  'Data Analyst',
  'Product Manager',
  'UI/UX Designer',
  'Marketing',
  'Business Analyst',
  'DevOps Engineer',
  'Full Stack Developer',
  'Backend Developer',
  'Frontend Developer'
];

const COMMON_SKILLS = [
  'Python', 'Java', 'JavaScript', 'React', 'Node.js',
  'SQL', 'MongoDB', 'AWS', 'Docker', 'Git',
  'HTML/CSS', 'TypeScript', 'C++', 'Data Structures',
  'Algorithms', 'Machine Learning', 'REST APIs'
];

function SmartOnboarding({ onComplete }) {
  const [activeStep, setActiveStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  
  const [formData, setFormData] = useState({
    year: '',
    branch: '',
    targetRole: '',
    skills: [],
    hoursPerWeek: '',
    customSkill: ''
  });

  const steps = ['Basic Info', 'Skills & Goals', 'Commitment'];

  const handleNext = () => {
    if (validateStep()) {
      setActiveStep((prev) => prev + 1);
    }
  };

  const handleBack = () => {
    setActiveStep((prev) => prev - 1);
  };

  const validateStep = () => {
    if (activeStep === 0) {
      if (!formData.year || !formData.branch) {
        setError('Please fill all fields');
        return false;
      }
    } else if (activeStep === 1) {
      if (!formData.targetRole || formData.skills.length === 0) {
        setError('Please select target role and at least one skill');
        return false;
      }
    } else if (activeStep === 2) {
      if (!formData.hoursPerWeek) {
        setError('Please specify hours per week');
        return false;
      }
    }
    setError('');
    return true;
  };

  const handleSkillToggle = (skill) => {
    setFormData(prev => ({
      ...prev,
      skills: prev.skills.includes(skill)
        ? prev.skills.filter(s => s !== skill)
        : [...prev.skills, skill]
    }));
  };

  const handleAddCustomSkill = () => {
    if (formData.customSkill && !formData.skills.includes(formData.customSkill)) {
      setFormData(prev => ({
        ...prev,
        skills: [...prev.skills, prev.customSkill],
        customSkill: ''
      }));
    }
  };

  const handleSubmit = async () => {
    if (!validateStep()) return;
    
    setLoading(true);
    try {
      const token = localStorage.getItem('token');
      
      // Update profile with onboarding data
      await axios.put(
        'http://localhost:8000/student/profile',
        {
          year: parseInt(formData.year),
          branch: formData.branch,
          target_role: formData.targetRole,
          skills: formData.skills,
          hours_per_week: parseInt(formData.hoursPerWeek)
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      // Generate initial learning plan
      await axios.post(
        'http://localhost:8000/plan/generate',
        {},
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );

      onComplete();
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to save profile');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 800, margin: 'auto', p: 3 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Card>
          <CardContent sx={{ p: 4 }}>
            <Typography variant="h4" gutterBottom align="center">
              🎯 Let's Personalize Your Journey
            </Typography>
            <Typography variant="body2" color="text.secondary" align="center" sx={{ mb: 4 }}>
              Tell us about yourself so Kai can create your perfect placement roadmap
            </Typography>

            <Stepper activeStep={activeStep} sx={{ mb: 4 }}>
              {steps.map((label) => (
                <Step key={label}>
                  <StepLabel>{label}</StepLabel>
                </Step>
              ))}
            </Stepper>

            {error && (
              <Alert severity="error" sx={{ mb: 2 }}>
                {error}
              </Alert>
            )}

            {/* Step 1: Basic Info */}
            {activeStep === 0 && (
              <Box>
                <TextField
                  select
                  fullWidth
                  label="Current Year"
                  value={formData.year}
                  onChange={(e) => setFormData({ ...formData, year: e.target.value })}
                  sx={{ mb: 3 }}
                >
                  <MenuItem value="1">1st Year</MenuItem>
                  <MenuItem value="2">2nd Year</MenuItem>
                  <MenuItem value="3">3rd Year</MenuItem>
                  <MenuItem value="4">4th Year</MenuItem>
                </TextField>

                <TextField
                  fullWidth
                  label="Branch/Department"
                  placeholder="e.g., Computer Science, Electronics, Mechanical"
                  value={formData.branch}
                  onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
                />
              </Box>
            )}

            {/* Step 2: Skills & Goals */}
            {activeStep === 1 && (
              <Box>
                <TextField
                  select
                  fullWidth
                  label="Target Role"
                  value={formData.targetRole}
                  onChange={(e) => setFormData({ ...formData, targetRole: e.target.value })}
                  sx={{ mb: 3 }}
                >
                  {ROLES.map((role) => (
                    <MenuItem key={role} value={role}>
                      {role}
                    </MenuItem>
                  ))}
                </TextField>

                <Typography variant="subtitle2" gutterBottom>
                  Select Your Current Skills
                </Typography>
                <Typography variant="caption" color="text.secondary" gutterBottom>
                  Choose all that apply
                </Typography>
                <Box sx={{ mt: 2, mb: 3 }}>
                  <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
                    {COMMON_SKILLS.map((skill) => (
                      <Chip
                        key={skill}
                        label={skill}
                        onClick={() => handleSkillToggle(skill)}
                        color={formData.skills.includes(skill) ? 'primary' : 'default'}
                        variant={formData.skills.includes(skill) ? 'filled' : 'outlined'}
                      />
                    ))}
                  </Stack>
                </Box>

                <Box sx={{ display: 'flex', gap: 1 }}>
                  <TextField
                    fullWidth
                    size="small"
                    label="Add Custom Skill"
                    value={formData.customSkill}
                    onChange={(e) => setFormData({ ...formData, customSkill: e.target.value })}
                    onKeyPress={(e) => e.key === 'Enter' && handleAddCustomSkill()}
                  />
                  <Button onClick={handleAddCustomSkill}>Add</Button>
                </Box>

                {formData.skills.length > 0 && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="caption" color="text.secondary">
                      Selected Skills:
                    </Typography>
                    <Box sx={{ mt: 1 }}>
                      <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
                        {formData.skills.map((skill) => (
                          <Chip
                            key={skill}
                            label={skill}
                            onDelete={() => handleSkillToggle(skill)}
                            color="primary"
                          />
                        ))}
                      </Stack>
                    </Box>
                  </Box>
                )}
              </Box>
            )}

            {/* Step 3: Commitment */}
            {activeStep === 2 && (
              <Box>
                <TextField
                  select
                  fullWidth
                  label="Hours Available Per Week"
                  value={formData.hoursPerWeek}
                  onChange={(e) => setFormData({ ...formData, hoursPerWeek: e.target.value })}
                  helperText="Be realistic - consistency matters more than quantity"
                >
                  <MenuItem value="5">5 hours (1 hour/day)</MenuItem>
                  <MenuItem value="10">10 hours (1-2 hours/day)</MenuItem>
                  <MenuItem value="15">15 hours (2-3 hours/day)</MenuItem>
                  <MenuItem value="20">20 hours (3-4 hours/day)</MenuItem>
                  <MenuItem value="25">25+ hours (4+ hours/day)</MenuItem>
                </TextField>

                <Alert severity="info" sx={{ mt: 3 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    What happens next?
                  </Typography>
                  <Typography variant="body2">
                    • Kai will generate your personalized 7-day action plan
                    <br />
                    • You'll get role-specific mock interview questions
                    <br />
                    • Daily tasks tailored to your available time
                    <br />
                    • Track your progress with Placement Readiness Score
                  </Typography>
                </Alert>
              </Box>
            )}

            {/* Navigation Buttons */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
              <Button
                disabled={activeStep === 0}
                onClick={handleBack}
              >
                Back
              </Button>
              <Box>
                {activeStep === steps.length - 1 ? (
                  <Button
                    variant="contained"
                    onClick={handleSubmit}
                    disabled={loading}
                    startIcon={loading && <CircularProgress size={20} />}
                  >
                    {loading ? 'Setting Up...' : 'Complete Setup'}
                  </Button>
                ) : (
                  <Button variant="contained" onClick={handleNext}>
                    Next
                  </Button>
                )}
              </Box>
            </Box>
          </CardContent>
        </Card>
      </motion.div>
    </Box>
  );
}

export default SmartOnboarding;
