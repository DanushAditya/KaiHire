import { Card, CardContent, Typography, Box, Chip, Button, Divider } from '@mui/material';
import { motion } from 'framer-motion';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment';
import SchoolIcon from '@mui/icons-material/School';
import WorkIcon from '@mui/icons-material/Work';
import ShareIcon from '@mui/icons-material/Share';

function ReadinessCard({ cardData, onShare }) {
  const getPRIColor = (score) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#2196f3';
    if (score >= 40) return '#ff9800';
    return '#f44336';
  };

  const getTierColor = (tier) => {
    const colors = {
      'Beginner': '#9e9e9e',
      'Explorer': '#2196f3',
      'Achiever': '#9c27b0',
      'Pro': '#ff9800',
      'Elite': '#ffd700'
    };
    return colors[tier] || '#9e9e9e';
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <Card 
        sx={{ 
          maxWidth: 600, 
          margin: 'auto',
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          borderRadius: 3,
          boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
        }}
      >
        <CardContent sx={{ p: 4 }}>
          {/* Header */}
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Typography variant="h5" fontWeight="bold" gutterBottom>
              Professional Readiness Card
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              KaiHire Placement Copilot
            </Typography>
          </Box>

          <Divider sx={{ bgcolor: 'rgba(255,255,255,0.3)', mb: 3 }} />

          {/* Student Info */}
          <Box sx={{ mb: 3 }}>
            <Typography variant="h4" fontWeight="bold" gutterBottom>
              {cardData.name}
            </Typography>
            <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap', mb: 1 }}>
              <Chip 
                icon={<SchoolIcon />} 
                label={cardData.college} 
                size="small"
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
              <Chip 
                label={`Year ${cardData.year} • ${cardData.branch}`} 
                size="small"
                sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
              />
            </Box>
            <Chip 
              icon={<WorkIcon />} 
              label={`Target: ${cardData.target_role}`} 
              sx={{ bgcolor: 'rgba(255,255,255,0.3)', color: 'white', fontWeight: 'bold' }}
            />
          </Box>

          {/* Scores */}
          <Box sx={{ 
            display: 'grid', 
            gridTemplateColumns: '1fr 1fr 1fr', 
            gap: 2, 
            mb: 3,
            textAlign: 'center'
          }}>
            <Box sx={{ 
              bgcolor: 'rgba(255,255,255,0.2)', 
              p: 2, 
              borderRadius: 2 
            }}>
              <Typography variant="h3" fontWeight="bold" sx={{ color: getPRIColor(cardData.pri_score) }}>
                {cardData.pri_score}
              </Typography>
              <Typography variant="caption">PRI Score</Typography>
            </Box>
            <Box sx={{ 
              bgcolor: 'rgba(255,255,255,0.2)', 
              p: 2, 
              borderRadius: 2 
            }}>
              <Typography variant="h3" fontWeight="bold">
                {cardData.sli_level}
              </Typography>
              <Typography variant="caption">Skill Level</Typography>
            </Box>
            <Box sx={{ 
              bgcolor: 'rgba(255,255,255,0.2)', 
              p: 2, 
              borderRadius: 2 
            }}>
              <LocalFireDepartmentIcon sx={{ fontSize: 40, color: '#ff6b6b' }} />
              <Typography variant="h4" fontWeight="bold">
                {cardData.current_streak}
              </Typography>
              <Typography variant="caption">Day Streak</Typography>
            </Box>
          </Box>

          {/* Tier Badge */}
          <Box sx={{ textAlign: 'center', mb: 3 }}>
            <Chip
              icon={<EmojiEventsIcon />}
              label={`${cardData.tier} Tier • ${cardData.total_xp} XP`}
              sx={{ 
                bgcolor: getTierColor(cardData.tier),
                color: 'white',
                fontWeight: 'bold',
                fontSize: '1rem',
                py: 2.5,
                px: 1
              }}
            />
          </Box>

          {/* Skills */}
          {cardData.top_skills && cardData.top_skills.length > 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" gutterBottom sx={{ opacity: 0.9 }}>
                Top Skills
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {cardData.top_skills.map((skill, index) => (
                  <Chip 
                    key={index}
                    label={skill} 
                    size="small"
                    sx={{ bgcolor: 'rgba(255,255,255,0.3)', color: 'white' }}
                  />
                ))}
              </Box>
            </Box>
          )}

          {/* Strengths */}
          {cardData.strength_areas && cardData.strength_areas.length > 0 && (
            <Box sx={{ mb: 2 }}>
              <Typography variant="subtitle2" gutterBottom sx={{ opacity: 0.9 }}>
                💪 Strengths
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {cardData.strength_areas.map((strength, index) => (
                  <Chip 
                    key={index}
                    label={strength} 
                    size="small"
                    sx={{ bgcolor: 'rgba(76, 175, 80, 0.3)', color: 'white' }}
                  />
                ))}
              </Box>
            </Box>
          )}

          {/* Improvements */}
          {cardData.improvement_areas && cardData.improvement_areas.length > 0 && (
            <Box sx={{ mb: 3 }}>
              <Typography variant="subtitle2" gutterBottom sx={{ opacity: 0.9 }}>
                🎯 Focus Areas
              </Typography>
              <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                {cardData.improvement_areas.map((area, index) => (
                  <Chip 
                    key={index}
                    label={area} 
                    size="small"
                    sx={{ bgcolor: 'rgba(255, 152, 0, 0.3)', color: 'white' }}
                  />
                ))}
              </Box>
            </Box>
          )}

          <Divider sx={{ bgcolor: 'rgba(255,255,255,0.3)', mb: 2 }} />

          {/* Referral Code */}
          <Box sx={{ textAlign: 'center', mb: 2 }}>
            <Typography variant="caption" sx={{ opacity: 0.9 }}>
              Referral Code
            </Typography>
            <Typography variant="h6" fontWeight="bold" sx={{ letterSpacing: 2 }}>
              {cardData.referral_code}
            </Typography>
          </Box>

          {/* Share Button */}
          <Button
            fullWidth
            variant="contained"
            startIcon={<ShareIcon />}
            onClick={onShare}
            sx={{
              bgcolor: 'rgba(255,255,255,0.2)',
              '&:hover': {
                bgcolor: 'rgba(255,255,255,0.3)'
              },
              color: 'white',
              fontWeight: 'bold'
            }}
          >
            Challenge a Friend
          </Button>
        </CardContent>
      </Card>
    </motion.div>
  );
}

export default ReadinessCard;
