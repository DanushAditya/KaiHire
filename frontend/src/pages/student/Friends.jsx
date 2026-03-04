import { useState, useEffect } from 'react';
import {
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  List,
  ListItem,
  ListItemText,
  Box,
  Alert,
  Chip,
} from '@mui/material';
import Layout from '../../components/Layout';
import { getFriends, sendFriendRequest, getFriendRequests, acceptFriendRequest } from '../../services/api';

function Friends({ toggleTheme, mode }) {
  const [friends, setFriends] = useState([]);
  const [requests, setRequests] = useState([]);
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchFriends();
    fetchRequests();
  }, []);

  const fetchFriends = async () => {
    try {
      const response = await getFriends();
      setFriends(response.data);
    } catch (error) {
      console.error('Error fetching friends:', error);
    }
  };

  const fetchRequests = async () => {
    try {
      const response = await getFriendRequests();
      setRequests(response.data);
    } catch (error) {
      console.error('Error fetching requests:', error);
    }
  };

  const handleSendRequest = async () => {
    try {
      await sendFriendRequest({ friend_email: email });
      setMessage('Friend request sent!');
      setEmail('');
    } catch (error) {
      setMessage('Error sending request');
    }
  };

  const handleAccept = async (friendshipId) => {
    try {
      await acceptFriendRequest(friendshipId);
      fetchFriends();
      fetchRequests();
      setMessage('Friend request accepted!');
    } catch (error) {
      setMessage('Error accepting request');
    }
  };

  return (
    <Layout toggleTheme={toggleTheme} mode={mode} role="STUDENT">
      <Typography variant="h4" gutterBottom>
        Friends
      </Typography>

      {message && <Alert severity="info" sx={{ mb: 2 }}>{message}</Alert>}

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Add Friend
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
            <TextField
              fullWidth
              label="Friend's Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
            <Button variant="contained" onClick={handleSendRequest}>
              Send Request
            </Button>
          </Box>
        </CardContent>
      </Card>

      {requests.length > 0 && (
        <Card sx={{ mt: 3 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Friend Requests
            </Typography>
            <List>
              {requests.map((request) => (
                <ListItem
                  key={request.id}
                  secondaryAction={
                    <Button
                      variant="contained"
                      size="small"
                      onClick={() => handleAccept(request.id)}
                    >
                      Accept
                    </Button>
                  }
                >
                  <ListItemText
                    primary={request.sender_name}
                    secondary={request.sender_email}
                  />
                </ListItem>
              ))}
            </List>
          </CardContent>
        </Card>
      )}

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            My Friends
          </Typography>
          <List>
            {friends.map((friend) => (
              <ListItem key={friend.id}>
                <ListItemText
                  primary={friend.name}
                  secondary={
                    <>
                      {friend.college} • {friend.target_role}
                      <br />
                      PRI: {friend.placement_readiness_index.toFixed(1)} • Streak: {friend.current_streak}
                    </>
                  }
                />
                <Chip label={friend.tier} size="small" />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Layout>
  );
}

export default Friends;
