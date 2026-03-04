import { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  Chip,
  LinearProgress,
  Box,
} from '@mui/material';
import Layout from '../../components/Layout';
import { getChallenges, getMyChallenges, enrollChallenge } from '../../services/api';

function Challenges({ toggleTheme, mode }) {
  const [challenges, setChallenges] = useState([]);
  const [myChallenges, setMyChallenges] = useState([]);

  useEffect(() => {
    fetchChallenges();
    fetchMyChallenges();
  }, []);

  const fetchChallenges = async () => {
    try {
      const response = await getChallenges();
      setChallenges(response.data);
    } catch (error) {
      console.error('Error fetching challenges:', error);
    }
  };

  const fetchMyChallenges = async () => {
    try {
      const response = await getMyChallenges();
      setMyChallenges(response.data);
    } catch (error) {
      console.error('Error fetching my challenges:', error);
    }
  };

  const handleEnroll = async (challengeId) => {
    try {
      await enrollChallenge({ challenge_id: challengeId });
      fetchMyChallenges();
    } catch (error) {
      console.error('Error enrolling:', error);
    }
  };

  const isEnrolled = (challengeId) => {
    return myChallenges.some(c => c.challenge_id === challengeId);
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Typography variant="h4" gutterBottom>
        Challenges
      </Typography>

      <Typography variant="h6" sx={{ mt: 3, mb: 2 }}>
        My Active Challenges
      </Typography>
      <Grid container spacing={3}>
        {myChallenges.filter(c => !c.is_completed).map((participation) => {
          const challenge = challenges.find(ch => ch.id === participation.challenge_id);
          return (
            <Grid item xs={12} md={6} key={participation.id}>
              <Card>
                <CardContent>
                  <Typography variant="h6">{challenge?.title}</Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {challenge?.description}
                  </Typography>
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body2">Progress: {participation.progress}%</Typography>
                    <LinearProgress variant="determinate" value={participation.progress} sx={{ mt: 1 }} />
                  </Box>
                  <Box sx={{ mt: 2 }}>
                    <Chip label={`${challenge?.xp_reward} XP`} size="small" color="primary" />
                    <Chip label={`+${challenge?.pri_boost} PRI`} size="small" color="secondary" sx={{ ml: 1 }} />
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          );
        })}
      </Grid>

      <Typography variant="h6" sx={{ mt: 4, mb: 2 }}>
        Available Challenges
      </Typography>
      <Grid container spacing={3}>
        {challenges.map((challenge) => (
          <Grid item xs={12} md={6} key={challenge.id}>
            <Card>
              <CardContent>
                <Typography variant="h6">{challenge.title}</Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                  {challenge.description}
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Chip label={challenge.challenge_type} size="small" />
                  <Chip label={challenge.difficulty} size="small" sx={{ ml: 1 }} />
                  <Chip label={`${challenge.duration_days} days`} size="small" sx={{ ml: 1 }} />
                </Box>
                <Box sx={{ mt: 2 }}>
                  <Chip label={`${challenge.xp_reward} XP`} size="small" color="primary" />
                  <Chip label={`+${challenge.pri_boost} PRI`} size="small" color="secondary" sx={{ ml: 1 }} />
                </Box>
                <Button
                  variant="contained"
                  fullWidth
                  sx={{ mt: 2 }}
                  disabled={isEnrolled(challenge.id)}
                  onClick={() => handleEnroll(challenge.id)}
                >
                  {isEnrolled(challenge.id) ? 'Enrolled' : 'Enroll Now'}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Layout>
  );
}

export default Challenges;
