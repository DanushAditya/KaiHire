import { useState, useEffect } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  Stack,
  Alert,
  CircularProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField
} from '@mui/material';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import RefreshIcon from '@mui/icons-material/Refresh';
import { motion } from 'framer-motion';
import Layout from '../../components/Layout';
import axios from 'axios';

function MockInterview({ toggleTheme, mode }) {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [answers, setAnswers] = useState({});
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/student/profile', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setProfile(response.data);
      generateQuestions(response.data.target_role);
    } catch (err) {
      console.error('Error fetching profile:', err);
    }
  };

  const generateQuestions = async (targetRole) => {
    setLoading(true);
    setError('');
    try {
      const token = localStorage.getItem('token');
      const response = await axios.post(
        'http://localhost:8000/ai/interview-questions',
        {
          target_role: targetRole || 'Software Developer',
          difficulty: 'medium',
          count: 10
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      );
      setQuestions(response.data.questions || []);
    } catch (err) {
      setError('Failed to generate questions. Make sure Ollama is running.');
      console.error('Error generating questions:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (index, value) => {
    setAnswers({ ...answers, [index]: value });
  };

  const getDifficultyColor = (difficulty) => {
    const colors = {
      easy: 'success',
      medium: 'warning',
      hard: 'error'
    };
    return colors[difficulty?.toLowerCase()] || 'default';
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Box sx={{ maxWidth: 1000, margin: 'auto' }}>
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box>
              <Typography variant="h4" gutterBottom>
                🎯 Mock Interview Questions
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Practice role-specific questions for {profile?.target_role || 'your target role'}
              </Typography>
            </Box>
            <Button
              variant="outlined"
              startIcon={<RefreshIcon />}
              onClick={() => generateQuestions(profile?.target_role)}
              disabled={loading}
            >
              New Set
            </Button>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          {loading ? (
            <Box sx={{ display: 'flex', justifyContent: 'center', py: 8 }}>
              <CircularProgress />
            </Box>
          ) : (
            <Stack spacing={2}>
              {questions.length === 0 ? (
                <Card>
                  <CardContent>
                    <Typography variant="body1" color="text.secondary" align="center">
                      Click "New Set" to generate interview questions
                    </Typography>
                  </CardContent>
                </Card>
              ) : (
                questions.map((q, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                  >
                    <Accordion>
                      <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, width: '100%' }}>
                          <Chip 
                            label={`Q${index + 1}`} 
                            size="small" 
                            color="primary"
                          />
                          {q.difficulty && (
                            <Chip 
                              label={q.difficulty} 
                              size="small" 
                              color={getDifficultyColor(q.difficulty)}
                            />
                          )}
                          {q.category && (
                            <Chip 
                              label={q.category} 
                              size="small" 
                              variant="outlined"
                            />
                          )}
                          <Typography sx={{ flex: 1 }}>
                            {q.question}
                          </Typography>
                        </Box>
                      </AccordionSummary>
                      <AccordionDetails>
                        <Stack spacing={2}>
                          {q.hint && (
                            <Alert severity="info">
                              <Typography variant="subtitle2">💡 Hint</Typography>
                              <Typography variant="body2">{q.hint}</Typography>
                            </Alert>
                          )}
                          
                          <TextField
                            fullWidth
                            multiline
                            rows={4}
                            placeholder="Type your answer here..."
                            value={answers[index] || ''}
                            onChange={(e) => handleAnswerChange(index, e.target.value)}
                            variant="outlined"
                          />

                          {q.sample_answer && (
                            <Accordion>
                              <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <Typography variant="subtitle2" color="success.main">
                                  ✓ View Sample Answer
                                </Typography>
                              </AccordionSummary>
                              <AccordionDetails>
                                <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap' }}>
                                  {q.sample_answer}
                                </Typography>
                              </AccordionDetails>
                            </Accordion>
                          )}

                          {q.key_points && q.key_points.length > 0 && (
                            <Box>
                              <Typography variant="subtitle2" gutterBottom>
                                Key Points to Cover:
                              </Typography>
                              <Stack spacing={0.5}>
                                {q.key_points.map((point, i) => (
                                  <Typography key={i} variant="body2" color="text.secondary">
                                    • {point}
                                  </Typography>
                                ))}
                              </Stack>
                            </Box>
                          )}
                        </Stack>
                      </AccordionDetails>
                    </Accordion>
                  </motion.div>
                ))
              )}
            </Stack>
          )}

          <Card sx={{ mt: 4, bgcolor: 'primary.light' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                💪 Pro Tips
              </Typography>
              <Stack spacing={1}>
                <Typography variant="body2">
                  • Practice answering out loud, not just in your head
                </Typography>
                <Typography variant="body2">
                  • Use the STAR method (Situation, Task, Action, Result) for behavioral questions
                </Typography>
                <Typography variant="body2">
                  • Time yourself - aim for 2-3 minutes per answer
                </Typography>
                <Typography variant="body2">
                  • Record yourself to identify areas for improvement
                </Typography>
              </Stack>
            </CardContent>
          </Card>
        </motion.div>
      </Box>
    </Layout>
  );
}

export default MockInterview;
