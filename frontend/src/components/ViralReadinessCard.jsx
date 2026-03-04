import { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip,
  Tooltip,
  CircularProgress,
  LinearProgress,
  Divider,
  Stack
} from '@mui/material';
import { motion } from 'framer-motion';
import DownloadIcon from '@mui/icons-material/Download';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import WhatsAppIcon from '@mui/icons-material/WhatsApp';
import TelegramIcon from '@mui/icons-material/Telegram';
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import html2canvas from 'html2canvas';

function ViralReadinessCard({ studentData }) {
  const [copied, setCopied] = useState(false);
  const [downloading, setDownloading] = useState(false);

  const shareUrl = `${window.location.origin}/register?ref=${studentData.referral_code}`;
  
  const getPRIColor = (score) => {
    if (score >= 80) return '#4caf50';
    if (score >= 60) return '#2196f3';
    if (score >= 40) return '#ff9800';
    return '#f44336';
  };

  const getTierEmoji = (tier) => {
    const emojis = {
      'Beginner': '🌱',
      'Explorer': '🚀',
      'Achiever': '⭐',
      'Pro': '💎',
      'Elite': '👑'
    };
    return emojis[tier] || '🌱';
  };

  const handleCopyLink = () => {
    navigator.clipboard.writeText(shareUrl);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleWhatsAppShare = () => {
    const text = `🎯 Check out my Placement Readiness Score: ${studentData.pri_score}/100!\n\n` +
                 `${getTierEmoji(studentData.tier)} ${studentData.tier} Tier | 🔥 ${studentData.current_streak} Day Streak\n\n` +
                 `Join KaiHire and track your placement readiness too!\n${shareUrl}`;
    window.open(`https://wa.me/?text=${encodeURIComponent(text)}`, '_blank');
  };

  const handleTelegramShare = () => {
    const text = `🎯 My Placement Readiness: ${studentData.pri_score}/100 | ${getTierEmoji(studentData.tier)} ${studentData.tier}`;
    window.open(`https://t.me/share/url?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(text)}`, '_blank');
  };

  const handleDownload = async () => {
    setDownloading(true);
    try {
      const element = document.getElementById('readiness-card');
      const canvas = await html2canvas(element, {
        backgroundColor: null,
        scale: 2
      });
      const link = document.createElement('a');
      link.download = `placement-readiness-${studentData.name.replace(/\s+/g, '-')}.png`;
      link.href = canvas.toDataURL();
      link.click();
    } catch (error) {
      console.error('Download failed:', error);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 600, margin: 'auto' }}>
      {/* Main Card */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        <Card 
          id="readiness-card"
          sx={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            borderRadius: 4,
            boxShadow: '0 20px 60px rgba(0,0,0,0.3)',
            position: 'relative',
            overflow: 'hidden'
          }}
        >
          {/* Decorative Elements */}
          <Box sx={{
            position: 'absolute',
            top: -50,
            right: -50,
            width: 200,
            height: 200,
            borderRadius: '50%',
            background: 'rgba(255,255,255,0.1)',
            filter: 'blur(40px)'
          }} />

          <CardContent sx={{ p: 4, position: 'relative', zIndex: 1 }}>
            {/* Header */}
            <Box sx={{ textAlign: 'center', mb: 3 }}>
              <Typography variant="overline" sx={{ opacity: 0.9, letterSpacing: 2 }}>
                KaiHire Placement Copilot
              </Typography>
              <Typography variant="h4" fontWeight="bold" sx={{ mt: 1 }}>
                Placement Readiness Card
              </Typography>
            </Box>

            {/* Student Info */}
            <Box sx={{ mb: 3 }}>
              <Typography variant="h5" fontWeight="bold" gutterBottom>
                {studentData.name}
              </Typography>
              <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
                <Chip 
                  label={studentData.college} 
                  size="small"
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                />
                <Chip 
                  label={`Year ${studentData.year} • ${studentData.branch}`} 
                  size="small"
                  sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                />
                <Chip 
                  label={`🎯 ${studentData.target_role}`} 
                  sx={{ bgcolor: 'rgba(255,255,255,0.3)', color: 'white', fontWeight: 'bold' }}
                />
              </Stack>
            </Box>

            {/* PRI Score - Big and Bold */}
            <Box sx={{ 
              textAlign: 'center', 
              my: 4,
              p: 3,
              bgcolor: 'rgba(255,255,255,0.15)',
              borderRadius: 3,
              backdropFilter: 'blur(10px)'
            }}>
              <Typography variant="overline" sx={{ opacity: 0.9 }}>
                Placement Readiness Index
              </Typography>
              <Box sx={{ position: 'relative', display: 'inline-flex', my: 2 }}>
                <CircularProgress
                  variant="determinate"
                  value={studentData.pri_score}
                  size={150}
                  thickness={4}
                  sx={{
                    color: getPRIColor(studentData.pri_score),
                    '& .MuiCircularProgress-circle': {
                      strokeLinecap: 'round',
                    }
                  }}
                />
                <Box
                  sx={{
                    top: 0,
                    left: 0,
                    bottom: 0,
                    right: 0,
                    position: 'absolute',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexDirection: 'column'
                  }}
                >
                  <Typography variant="h2" fontWeight="bold">
                    {studentData.pri_score}
                  </Typography>
                  <Typography variant="caption">out of 100</Typography>
                </Box>
              </Box>
              <Typography variant="h6" sx={{ mt: 1 }}>
                {studentData.pri_score >= 80 ? '🔥 Placement Ready!' :
                 studentData.pri_score >= 60 ? '💪 Almost There!' :
                 studentData.pri_score >= 40 ? '📈 Good Progress!' :
                 '🌱 Keep Building!'}
              </Typography>
            </Box>

            {/* Stats Grid */}
            <Box sx={{ 
              display: 'grid', 
              gridTemplateColumns: '1fr 1fr 1fr', 
              gap: 2, 
              mb: 3 
            }}>
              <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                <Typography variant="h6">{getTierEmoji(studentData.tier)}</Typography>
                <Typography variant="h6" fontWeight="bold">{studentData.tier}</Typography>
                <Typography variant="caption">Tier</Typography>
              </Box>
              <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                <LocalFireDepartmentIcon sx={{ fontSize: 30, color: '#ff6b6b' }} />
                <Typography variant="h6" fontWeight="bold">{studentData.current_streak}</Typography>
                <Typography variant="caption">Day Streak</Typography>
              </Box>
              <Box sx={{ textAlign: 'center', p: 2, bgcolor: 'rgba(255,255,255,0.1)', borderRadius: 2 }}>
                <TrendingUpIcon sx={{ fontSize: 30 }} />
                <Typography variant="h6" fontWeight="bold">{studentData.total_xp}</Typography>
                <Typography variant="caption">Total XP</Typography>
              </Box>
            </Box>

            {/* Skills */}
            {studentData.top_skills && studentData.top_skills.length > 0 && (
              <Box sx={{ mb: 3 }}>
                <Typography variant="subtitle2" gutterBottom sx={{ opacity: 0.9 }}>
                  💻 Top Skills
                </Typography>
                <Stack direction="row" spacing={1} flexWrap="wrap" gap={1}>
                  {studentData.top_skills.slice(0, 5).map((skill, index) => (
                    <Chip 
                      key={index}
                      label={skill} 
                      size="small"
                      sx={{ bgcolor: 'rgba(255,255,255,0.25)', color: 'white' }}
                    />
                  ))}
                </Stack>
              </Box>
            )}

            {/* Strengths & Focus */}
            <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2, mb: 3 }}>
              {studentData.strength_areas && studentData.strength_areas.length > 0 && (
                <Box>
                  <Typography variant="caption" sx={{ opacity: 0.9 }}>
                    💪 Strengths
                  </Typography>
                  {studentData.strength_areas.slice(0, 2).map((strength, index) => (
                    <Typography key={index} variant="body2" sx={{ fontSize: '0.85rem', mt: 0.5 }}>
                      • {strength}
                    </Typography>
                  ))}
                </Box>
              )}
              {studentData.improvement_areas && studentData.improvement_areas.length > 0 && (
                <Box>
                  <Typography variant="caption" sx={{ opacity: 0.9 }}>
                    🎯 Focus On
                  </Typography>
                  {studentData.improvement_areas.slice(0, 2).map((area, index) => (
                    <Typography key={index} variant="body2" sx={{ fontSize: '0.85rem', mt: 0.5 }}>
                      • {area}
                    </Typography>
                  ))}
                </Box>
              )}
            </Box>

            <Divider sx={{ bgcolor: 'rgba(255,255,255,0.3)', my: 3 }} />

            {/* Referral Section */}
            <Box sx={{ textAlign: 'center', mb: 2 }}>
              <Typography variant="caption" sx={{ opacity: 0.9 }}>
                🎁 Challenge Your Friends
              </Typography>
              <Box sx={{ 
                mt: 1, 
                p: 2, 
                bgcolor: 'rgba(255,255,255,0.15)', 
                borderRadius: 2,
                border: '2px dashed rgba(255,255,255,0.3)'
              }}>
                <Typography variant="overline" sx={{ opacity: 0.8 }}>
                  Your Referral Code
                </Typography>
                <Typography variant="h5" fontWeight="bold" sx={{ letterSpacing: 3, my: 1 }}>
                  {studentData.referral_code}
                </Typography>
                <Typography variant="caption" sx={{ opacity: 0.9 }}>
                  Both get +50 XP bonus! 🎉
                </Typography>
              </Box>
            </Box>
          </CardContent>
        </Card>
      </motion.div>

      {/* Share Actions */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
      >
        <Card sx={{ mt: 2, p: 2 }}>
          <Typography variant="subtitle2" gutterBottom align="center" color="text.secondary">
            📢 Share Your Achievement
          </Typography>
          <Stack direction="row" spacing={1} justifyContent="center" flexWrap="wrap" gap={1}>
            <Tooltip title={copied ? "Copied!" : "Copy Link"}>
              <Button
                variant="outlined"
                startIcon={<ContentCopyIcon />}
                onClick={handleCopyLink}
                color={copied ? "success" : "primary"}
              >
                {copied ? "Copied!" : "Copy Link"}
              </Button>
            </Tooltip>
            
            <Button
              variant="contained"
              startIcon={<WhatsAppIcon />}
              onClick={handleWhatsAppShare}
              sx={{ 
                bgcolor: '#25D366', 
                '&:hover': { bgcolor: '#20BA5A' }
              }}
            >
              WhatsApp
            </Button>
            
            <Button
              variant="contained"
              startIcon={<TelegramIcon />}
              onClick={handleTelegramShare}
              sx={{ 
                bgcolor: '#0088cc', 
                '&:hover': { bgcolor: '#006699' }
              }}
            >
              Telegram
            </Button>
            
            <Button
              variant="outlined"
              startIcon={downloading ? <CircularProgress size={20} /> : <DownloadIcon />}
              onClick={handleDownload}
              disabled={downloading}
            >
              Download
            </Button>
          </Stack>

          {/* Viral Message */}
          <Box sx={{ 
            mt: 2, 
            p: 2, 
            bgcolor: 'success.light', 
            borderRadius: 2,
            textAlign: 'center'
          }}>
            <Typography variant="body2" color="success.dark" fontWeight="medium">
              🎯 Share with 3 friends and unlock Premium Features!
            </Typography>
            <LinearProgress 
              variant="determinate" 
              value={33} 
              sx={{ mt: 1, height: 8, borderRadius: 4 }}
            />
            <Typography variant="caption" color="text.secondary">
              1 of 3 friends joined
            </Typography>
          </Box>
        </Card>
      </motion.div>
    </Box>
  );
}

export default ViralReadinessCard;
