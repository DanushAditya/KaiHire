import { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  LinearProgress,
  Chip,
  Button,
} from '@mui/material';
import {
  TrendingUp,
  EmojiEvents,
  LocalFireDepartment,
  Star,
} from '@mui/icons-material';
import { motion } from 'framer-motion';
import Layout from '../../components/Layout';
import ViralReadinessCard from '../../components/ViralReadinessCard';
import { getStudentProfile } from '../../services/api';
import axios from 'axios';

function Dashboard({ toggleTheme, mode }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [cardData, setCardData] = useState(null);
  const [showCard, setShowCard] = useState(false);

  useEffect(() => {
    fetchProfile();
  }, []);

  const fetchProfile = async () => {
    try {
      const response = await getStudentProfile();
      setProfile(response.data);
    } catch (error) {
      console.error('Error fetching profile:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateCard = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('http://localhost:8000/card/generate', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setCardData(response.data.card);
      setShowCard(true);
    } catch (error) {
      console.error('Error generating card:', error);
    }
  };

  if (loading) {
    return (
      <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
        <Box sx={{ width: '100%' }}>
          <LinearProgress />
        </Box>
      </Layout>
    );
  }

  const StatCard = ({ title, value, icon, color }) => (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Card>
        <CardContent>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Box>
              <Typography color="text.secondary" gutterBottom>
                {title}
              </Typography>
              <Typography variant="h4" component="div">
                {value}
              </Typography>
            </Box>
            <Box sx={{ color, fontSize: 40 }}>
              {icon}
            </Box>
          </Box>
        </CardContent>
      </Card>
    </motion.div>
  );

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Typography variant="h4" gutterBottom>
        Welcome back, {profile?.name}!
      </Typography>
      
      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="PRI Score"
            value={profile?.placement_readiness_index?.toFixed(1) || 0}
            icon={<TrendingUp />}
            color="primary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="SLI Score"
            value={profile?.skill_level_index?.toFixed(1) || 0}
            icon={<Star />}
            color="secondary.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Current Streak"
            value={`${profile?.current_streak || 0} days`}
            icon={<LocalFireDepartment />}
            color="error.main"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total XP"
            value={profile?.total_xp || 0}
            icon={<EmojiEvents />}
            color="warning.main"
          />
        </Grid>
      </Grid>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Profile Overview
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  College: {profile?.college}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Branch: {profile?.branch} - Year {profile?.year}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Target Role: {profile?.target_role}
                </Typography>
                <Box sx={{ mt: 1, display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Tier:
                  </Typography>
                  <Chip label={profile?.tier} size="small" color="primary" />
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Skills
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                {profile?.skills?.length > 0 ? (
                  profile.skills.map((skill, index) => (
                    <Chip key={index} label={skill} size="small" />
                  ))
                ) : (
                  <Typography variant="body2" color="text.secondary">
                    No skills added yet
                  </Typography>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Quick Actions
              </Typography>
              <Box sx={{ mt: 2, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
                <Button variant="contained" href="/student/profile">
                  Update Profile
                </Button>
                <Button variant="outlined" href="/student/plan">
                  View My Plan
                </Button>
                <Button variant="outlined" href="/student/challenges">
                  Take Challenge
                </Button>
                <Button 
                  variant="contained" 
                  color="secondary"
                  onClick={handleGenerateCard}
                >
                  🎯 Generate Readiness Card
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Viral Readiness Card */}
        {showCard && cardData && (
          <Grid item xs={12}>
            <ViralReadinessCard studentData={cardData} />
          </Grid>
        )}
      </Grid>
    </Layout>
  );
}

export default Dashboard;
