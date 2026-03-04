import { useState, useEffect } from 'react';
import {
  Container,
  Paper,
  Typography,
  Button,
  Box,
  Radio,
  RadioGroup,
  FormControlLabel,
  FormControl,
  LinearProgress,
  Card,
  CardContent,
  Chip,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { motion } from 'framer-motion';
import Layout from '../../components/Layout';
import api from '../../services/api';
import QuizIcon from '@mui/icons-material/Quiz';
import TimerIcon from '@mui/icons-material/Timer';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

function Assessment({ toggleTheme, mode }) {
  const [step, setStep] = useState('select'); // select, quiz, result
  const [category, setCategory] = useState('DSA');
  const [role, setRole] = useState('SDE');
  const [difficulty, setDifficulty] = useState('medium');
  const [questions, setQuestions] = useState([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answers, setAnswers] = useState({});
  const [timeLeft, setTimeLeft] = useState(600); // 10 minutes
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    if (step === 'quiz' && timeLeft > 0) {
      const timer = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            handleSubmit();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [step, timeLeft]);

  const fetchHistory = async () => {
    try {
      const response = await api.get('/assessment/history');
      setHistory(response.data.assessments || []);
    } catch (error) {
      console.error('Error fetching history:', error);
    }
  };

  const startAssessment = async () => {
    setLoading(true);
    try {
      const response = await api.post('/assessment/start', {
        category,
        role,
        difficulty
      });
      setQuestions(response.data.questions);
      setTimeLeft(response.data.time_limit);
      setStep('quiz');
      setCurrentQuestion(0);
      setAnswers({});
    } catch (error) {
      console.error('Error starting assessment:', error);
      alert('Failed to start assessment');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, answerIndex) => {
    setAnswers(prev => ({
      ...prev,
      [questionId]: answerIndex
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    try {
      const response = await api.post('/assessment/submit', {
        category,
        role,
        difficulty,
        answers,
        time_taken: 600 - timeLeft
      });
      setResult(response.data);
      setStep('result');
      fetchHistory();
    } catch (error) {
      console.error('Error submitting assessment:', error);
      alert('Failed to submit assessment');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const renderSelection = () => (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Paper sx={{ p: 4 }}>
          <Box sx={{ textAlign: 'center', mb: 4 }}>
            <QuizIcon sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" gutterBottom>
              Skill Assessment
            </Typography>
            <Typography color="text.secondary">
              Test your knowledge and improve your Skill Level Index
            </Typography>
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Select Category
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {['DSA', 'Python', 'Machine Learning', 'Web Development', 'Database'].map(cat => (
                <Chip
                  key={cat}
                  label={cat}
                  onClick={() => setCategory(cat)}
                  color={category === cat ? 'primary' : 'default'}
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Box>

          <Box sx={{ mb: 3 }}>
            <Typography variant="subtitle1" gutterBottom>
              Target Role
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
              {['SDE', 'ML', 'Analyst', 'Core'].map(r => (
                <Chip
                  key={r}
                  label={r}
                  onClick={() => setRole(r)}
                  color={role === r ? 'primary' : 'default'}
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Box>

          <Box sx={{ mb: 4 }}>
            <Typography variant="subtitle1" gutterBottom>
              Difficulty
            </Typography>
            <Box sx={{ display: 'flex', gap: 1 }}>
              {['easy', 'medium', 'hard'].map(diff => (
                <Chip
                  key={diff}
                  label={diff.charAt(0).toUpperCase() + diff.slice(1)}
                  onClick={() => setDifficulty(diff)}
                  color={difficulty === diff ? 'primary' : 'default'}
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Box>

          <Button
            fullWidth
            variant="contained"
            size="large"
            onClick={startAssessment}
            disabled={loading}
          >
            Start Assessment
          </Button>
        </Paper>

        {/* History */}
        {history.length > 0 && (
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Recent Assessments
            </Typography>
            {history.slice(0, 5).map((assessment, index) => (
              <Card key={index} sx={{ mb: 2 }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Box>
                      <Typography variant="subtitle1">
                        {assessment.category} - {assessment.difficulty}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(assessment.created_at).toLocaleDateString()}
                      </Typography>
                    </Box>
                    <Chip
                      label={`${assessment.score}%`}
                      color={assessment.score >= 70 ? 'success' : assessment.score >= 50 ? 'warning' : 'error'}
                    />
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Paper>
        )}
      </motion.div>
    </Container>
  );

  const renderQuiz = () => {
    const question = questions[currentQuestion];
    const progress = ((currentQuestion + 1) / questions.length) * 100;

    return (
      <Container maxWidth="md" sx={{ mt: 4 }}>
        <Paper sx={{ p: 4 }}>
          {/* Header */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
            <Typography variant="h6">
              Question {currentQuestion + 1} of {questions.length}
            </Typography>
            <Chip
              icon={<TimerIcon />}
              label={formatTime(timeLeft)}
              color={timeLeft < 60 ? 'error' : 'primary'}
            />
          </Box>

          <LinearProgress variant="determinate" value={progress} sx={{ mb: 3 }} />

          {/* Question */}
          <Typography variant="h5" gutterBottom sx={{ mb: 3 }}>
            {question.question_text}
          </Typography>

          {/* Options */}
          <FormControl component="fieldset" fullWidth>
            <RadioGroup
              value={answers[question.id] ?? ''}
              onChange={(e) => handleAnswer(question.id, parseInt(e.target.value))}
            >
              {question.options.map((option, index) => (
                <Paper
                  key={index}
                  sx={{
                    p: 2,
                    mb: 2,
                    cursor: 'pointer',
                    border: answers[question.id] === index ? 2 : 1,
                    borderColor: answers[question.id] === index ? 'primary.main' : 'divider',
                    '&:hover': {
                      bgcolor: 'action.hover'
                    }
                  }}
                  onClick={() => handleAnswer(question.id, index)}
                >
                  <FormControlLabel
                    value={index}
                    control={<Radio />}
                    label={option}
                    sx={{ width: '100%', m: 0 }}
                  />
                </Paper>
              ))}
            </RadioGroup>
          </FormControl>

          {/* Navigation */}
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 4 }}>
            <Button
              variant="outlined"
              onClick={() => setCurrentQuestion(prev => Math.max(0, prev - 1))}
              disabled={currentQuestion === 0}
            >
              Previous
            </Button>
            {currentQuestion < questions.length - 1 ? (
              <Button
                variant="contained"
                onClick={() => setCurrentQuestion(prev => prev + 1)}
              >
                Next
              </Button>
            ) : (
              <Button
                variant="contained"
                color="success"
                onClick={handleSubmit}
                disabled={loading}
              >
                Submit Assessment
              </Button>
            )}
          </Box>
        </Paper>
      </Container>
    );
  };

  const renderResult = () => (
    <Container maxWidth="md" sx={{ mt: 4 }}>
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
      >
        <Paper sx={{ p: 4, textAlign: 'center' }}>
          <CheckCircleIcon sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
          <Typography variant="h4" gutterBottom>
            Assessment Complete!
          </Typography>
          <Typography variant="body1" color="text.secondary" gutterBottom>
            {result?.message}
          </Typography>

          <Box sx={{ my: 4 }}>
            <Typography variant="h2" color="primary" gutterBottom>
              {result?.score}%
            </Typography>
            <Typography variant="body1">
              {result?.correct} out of {result?.total} correct
            </Typography>
          </Box>

          <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 4 }}>
            <Card>
              <CardContent>
                <Typography variant="h6">{result?.xp_earned}</Typography>
                <Typography variant="body2" color="text.secondary">
                  XP Earned {result?.bonus_xp > 0 && `(+${result.bonus_xp} bonus!)`}
                </Typography>
              </CardContent>
            </Card>
            <Card>
              <CardContent>
                <Typography variant="h6">{result?.tier}</Typography>
                <Typography variant="body2" color="text.secondary">Current Tier</Typography>
              </CardContent>
            </Card>
            <Card>
              <CardContent>
                <Typography variant="h6">{result?.new_sli?.toFixed(1)}</Typography>
                <Typography variant="body2" color="text.secondary">Skill Level Index</Typography>
              </CardContent>
            </Card>
            <Card>
              <CardContent>
                <Typography variant="h6">{result?.new_pri?.toFixed(1)}</Typography>
                <Typography variant="body2" color="text.secondary">Placement Readiness</Typography>
              </CardContent>
            </Card>
          </Box>

          {/* Detailed Results */}
          {result?.detailed_results && result.detailed_results.length > 0 && (
            <Box sx={{ mb: 4, textAlign: 'left' }}>
              <Typography variant="h6" gutterBottom>
                📊 Detailed Results
              </Typography>
              {result.detailed_results.map((item, index) => (
                <Card key={index} sx={{ mb: 2, bgcolor: item.is_correct ? 'success.light' : 'error.light' }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                      {item.is_correct ? (
                        <CheckCircleIcon color="success" />
                      ) : (
                        <Typography color="error">✗</Typography>
                      )}
                      <Typography variant="subtitle2">
                        Question {index + 1}
                      </Typography>
                    </Box>
                    <Typography variant="body2" sx={{ mb: 1 }}>
                      <strong>Q:</strong> {item.question_text}
                    </Typography>
                    <Typography variant="body2" sx={{ mb: 0.5 }}>
                      <strong>Your Answer:</strong> {item.user_answer}
                    </Typography>
                    {!item.is_correct && (
                      <Typography variant="body2" color="success.dark">
                        <strong>Correct Answer:</strong> {item.correct_answer}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              ))}
            </Box>
          )}

          {/* Improvement Suggestions */}
          {result?.improvements && result.improvements.length > 0 && (
            <Box sx={{ mb: 4, textAlign: 'left' }}>
              <Typography variant="h6" gutterBottom>
                💡 Improvement Suggestions
              </Typography>
              <Card>
                <CardContent>
                  {result.improvements.map((suggestion, index) => (
                    <Typography key={index} variant="body2" sx={{ mb: 1 }}>
                      • {suggestion}
                    </Typography>
                  ))}
                </CardContent>
              </Card>
            </Box>
          )}

          <Box sx={{ display: 'flex', gap: 2 }}>
            <Button
              fullWidth
              variant="outlined"
              onClick={() => {
                setStep('select');
                setResult(null);
              }}
            >
              Take Another Assessment
            </Button>
            <Button
              fullWidth
              variant="contained"
              onClick={() => window.location.href = '/student/dashboard'}
            >
              Back to Dashboard
            </Button>
          </Box>
        </Paper>
      </motion.div>
    </Container>
  );

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      {step === 'select' && renderSelection()}
      {step === 'quiz' && renderQuiz()}
      {step === 'result' && renderResult()}
    </Layout>
  );
}

export default Assessment;
