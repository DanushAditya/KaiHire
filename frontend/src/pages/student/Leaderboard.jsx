import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tabs,
  Tab,
  Box,
} from '@mui/material';
import Layout from '../../components/Layout';
import { getClassLeaderboard, getBranchLeaderboard, getCollegeLeaderboard, getStudentProfile } from '../../services/api';

function Leaderboard({ toggleTheme, mode }) {
  const [tab, setTab] = useState(0);
  const [leaderboard, setLeaderboard] = useState([]);
  const [profile, setProfile] = useState(null);

  useEffect(() => {
    fetchProfile();
  }, []);

  useEffect(() => {
    if (profile) {
      fetchLeaderboard();
    }
  }, [tab, profile]);

  const fetchProfile = async () => {
    try {
      const response = await getStudentProfile();
      setProfile(response.data);
    } catch (error) {
      console.error('Error fetching profile:', error);
    }
  };

  const fetchLeaderboard = async () => {
    if (!profile) return;

    try {
      let response;
      if (tab === 0) {
        response = await getClassLeaderboard({
          college: profile.college,
          branch: profile.branch,
          year: profile.year,
          section: profile.section,
        });
      } else if (tab === 1) {
        response = await getBranchLeaderboard({
          college: profile.college,
          branch: profile.branch,
        });
      } else {
        response = await getCollegeLeaderboard({
          college: profile.college,
        });
      }
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Typography variant="h4" gutterBottom>
        Leaderboard
      </Typography>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Tabs value={tab} onChange={(e, newValue) => setTab(newValue)}>
            <Tab label="Class" />
            <Tab label="Branch" />
            <Tab label="College" />
          </Tabs>

          <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Rank</TableCell>
                  <TableCell>Name</TableCell>
                  <TableCell>Target Role</TableCell>
                  <TableCell>PRI</TableCell>
                  <TableCell>Streak</TableCell>
                  <TableCell>Tier</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {leaderboard.map((student) => (
                  <TableRow key={student.rank}>
                    <TableCell>{student.rank}</TableCell>
                    <TableCell>{student.name}</TableCell>
                    <TableCell>{student.target_role}</TableCell>
                    <TableCell>{student.placement_readiness_index.toFixed(1)}</TableCell>
                    <TableCell>{student.current_streak}</TableCell>
                    <TableCell>{student.tier}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Layout>
  );
}

export default Leaderboard;
