import { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
} from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import Layout from '../../components/Layout';
import { getAnalytics } from '../../services/api';

function Analytics({ toggleTheme, mode }) {
  const [analytics, setAnalytics] = useState(null);

  useEffect(() => {
    fetchAnalytics();
  }, []);

  const fetchAnalytics = async () => {
    try {
      const response = await getAnalytics();
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching analytics:', error);
    }
  };

  if (!analytics) return null;

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="HR">
      <Typography variant="h4" gutterBottom>
        Analytics
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Colleges
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics.top_colleges}>
                  <XAxis dataKey="college" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#82ca9d" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Top Skills in Demand
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={analytics.top_skills}>
                  <XAxis dataKey="skill" />
                  <YAxis />
                  <Tooltip />
                  <Bar dataKey="count" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Key Metrics
              </Typography>
              <Typography variant="body1" sx={{ mt: 2 }}>
                Total Students: {analytics.total_students}
              </Typography>
              <Typography variant="body1">
                Average PRI: {analytics.average_pri}
              </Typography>
              <Typography variant="body1">
                Average Streak: {analytics.average_streak} days
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Tier Distribution
              </Typography>
              {analytics.tier_distribution.map((tier) => (
                <Typography key={tier.tier} variant="body1" sx={{ mt: 1 }}>
                  {tier.tier}: {tier.count} students
                </Typography>
              ))}
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Layout>
  );
}

export default Analytics;
