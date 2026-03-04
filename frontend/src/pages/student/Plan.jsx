import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Button,
  Box,
  List,
  ListItem,
  ListItemText,
  Checkbox,
  Chip,
  Alert,
} from '@mui/material';
import Layout from '../../components/Layout';
import { getPlans, getPlanTasks, generatePlan, completeTask } from '../../services/api';

function Plan({ toggleTheme, mode }) {
  const [plans, setPlans] = useState([]);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchPlans();
  }, []);

  const fetchPlans = async () => {
    try {
      const response = await getPlans();
      setPlans(response.data);
      if (response.data.length > 0) {
        loadPlanTasks(response.data[0].id);
      }
    } catch (error) {
      console.error('Error fetching plans:', error);
    }
  };

  const loadPlanTasks = async (planId) => {
    try {
      const response = await getPlanTasks(planId);
      setTasks(response.data);
      setSelectedPlan(planId);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  const handleGeneratePlan = async (planType) => {
    try {
      await generatePlan(planType);
      setMessage(`${planType === '7_day' ? '7-Day' : '30-Day'} plan generated!`);
      fetchPlans();
    } catch (error) {
      setMessage('Error generating plan');
    }
  };

  const handleCompleteTask = async (taskId) => {
    try {
      await completeTask(taskId);
      loadPlanTasks(selectedPlan);
      setMessage('Task completed! XP awarded.');
    } catch (error) {
      setMessage('Error completing task');
    }
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Typography variant="h4" gutterBottom>
        My Learning Plan
      </Typography>

      {message && <Alert severity="info" sx={{ mb: 2 }}>{message}</Alert>}

      {plans.length === 0 ? (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              No Plan Yet
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              Generate your personalized learning plan to get started!
            </Typography>
            <Button
              variant="contained"
              onClick={() => handleGeneratePlan('7_day')}
              sx={{ mt: 2 }}
            >
              Generate 7-Day Kickstart Plan
            </Button>
          </CardContent>
        </Card>
      ) : (
        <>
          <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
            {plans.map((plan) => (
              <Button
                key={plan.id}
                variant={selectedPlan === plan.id ? 'contained' : 'outlined'}
                onClick={() => loadPlanTasks(plan.id)}
              >
                {plan.plan_type === '7_day_kickstart' ? '7-Day Plan' : '30-Day Plan'}
                {plan.is_completed && <Chip label="Completed" size="small" sx={{ ml: 1 }} />}
              </Button>
            ))}
            {!plans.some(p => p.plan_type === '30_day_advanced') && (
              <Button
                variant="outlined"
                onClick={() => handleGeneratePlan('30_day')}
              >
                Unlock 30-Day Plan
              </Button>
            )}
          </Box>

          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tasks
              </Typography>
              <List>
                {tasks.map((task) => (
                  <ListItem
                    key={task.id}
                    secondaryAction={
                      !task.is_completed && (
                        <Button
                          size="small"
                          onClick={() => handleCompleteTask(task.id)}
                        >
                          Complete
                        </Button>
                      )
                    }
                  >
                    <Checkbox checked={task.is_completed} disabled />
                    <ListItemText
                      primary={`Day ${task.day}: ${task.title}`}
                      secondary={`${task.description} • ${task.xp_reward} XP`}
                    />
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </>
      )}
    </Layout>
  );
}

export default Plan;
