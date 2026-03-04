import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Box,
  Chip,
} from '@mui/material';
import Layout from '../../components/Layout';
import { filterStudents, exportStudents } from '../../services/api';

function TalentList({ toggleTheme, mode }) {
  const [students, setStudents] = useState([]);
  const [filters, setFilters] = useState({
    college: '',
    branch: '',
    year: '',
    min_pri: '',
    target_role: '',
  });

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const params = {};
      Object.keys(filters).forEach(key => {
        if (filters[key]) params[key] = filters[key];
      });
      const response = await filterStudents(params);
      setStudents(response.data);
    } catch (error) {
      console.error('Error fetching students:', error);
    }
  };

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const handleExport = async () => {
    try {
      const params = {};
      Object.keys(filters).forEach(key => {
        if (filters[key]) params[key] = filters[key];
      });
      const response = await exportStudents(params);
      
      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'students.csv');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Error exporting:', error);
    }
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="HR">
      <Typography variant="h4" gutterBottom>
        Talent List
      </Typography>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Filters
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap', mt: 2 }}>
            <TextField
              label="College"
              name="college"
              value={filters.college}
              onChange={handleFilterChange}
            />
            <TextField
              label="Branch"
              name="branch"
              value={filters.branch}
              onChange={handleFilterChange}
            />
            <TextField
              label="Year"
              name="year"
              type="number"
              value={filters.year}
              onChange={handleFilterChange}
            />
            <TextField
              label="Min PRI"
              name="min_pri"
              type="number"
              value={filters.min_pri}
              onChange={handleFilterChange}
            />
            <TextField
              label="Target Role"
              name="target_role"
              value={filters.target_role}
              onChange={handleFilterChange}
            />
          </Box>
          <Box sx={{ mt: 2, display: 'flex', gap: 2 }}>
            <Button variant="contained" onClick={fetchStudents}>
              Apply Filters
            </Button>
            <Button variant="outlined" onClick={handleExport}>
              Export CSV
            </Button>
          </Box>
        </CardContent>
      </Card>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Students ({students.length})
          </Typography>
          <TableContainer component={Paper} sx={{ mt: 2 }}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Email</TableCell>
                  <TableCell>College</TableCell>
                  <TableCell>Branch</TableCell>
                  <TableCell>Year</TableCell>
                  <TableCell>Target Role</TableCell>
                  <TableCell>PRI</TableCell>
                  <TableCell>SLI</TableCell>
                  <TableCell>Tier</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {students.map((student) => (
                  <TableRow key={student.id}>
                    <TableCell>{student.name}</TableCell>
                    <TableCell>{student.email}</TableCell>
                    <TableCell>{student.college}</TableCell>
                    <TableCell>{student.branch}</TableCell>
                    <TableCell>{student.year}</TableCell>
                    <TableCell>{student.target_role}</TableCell>
                    <TableCell>{student.placement_readiness_index.toFixed(1)}</TableCell>
                    <TableCell>{student.skill_level_index.toFixed(1)}</TableCell>
                    <TableCell>
                      <Chip label={student.tier} size="small" />
                    </TableCell>
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

export default TalentList;
