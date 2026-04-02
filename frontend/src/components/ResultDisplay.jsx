import React from 'react';
import { Paper, Typography, LinearProgress, Box, Chip, Button } from '@mui/material';
import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';

const ResultDisplay = ({ prediction, onReset }) => {
  const { will_churn, churn_probability, confidence, recommendation } = prediction;
  const probability = churn_probability * 100;
  const isHighRisk = will_churn === 'Yes';

  const chartData = [
    { name: 'Churn', value: churn_probability },
    { name: 'Stay', value: 1 - churn_probability },
  ];

  const COLORS = isHighRisk 
    ? ['#FB7185', '#475569']
    : ['#34D399', '#475569'];

  return (
    <Paper 
      elevation={0}
      className={isHighRisk ? 'glow-red-soft' : 'glow-green-soft'}
      sx={{ 
        p: 4, 
        background: 'rgba(30, 41, 59, 0.7)',
        backdropFilter: 'blur(12px) saturate(180%)',
        borderRadius: 3,
        position: 'relative',
        height: '100%',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'space-between',
      }}
    >
      {/* Close Button */}
      <Button
        onClick={onReset}
        sx={{
          position: 'absolute',
          top: 12,
          right: 12,
          minWidth: 'auto',
          padding: '4px 10px',
          color: 'rgba(248, 250, 252, 0.7)',
          backgroundColor: 'rgba(15, 23, 42, 0.5)',
          border: '1px solid rgba(248, 250, 252, 0.1)',
          borderRadius: 1.5,
          fontSize: '0.8rem',
          '&:hover': {
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            color: '#38BDF8',
          },
        }}
      >
        ✕
      </Button>

      <Box textAlign="center">
        <Typography 
          variant="h5" 
          sx={{
            fontWeight: 800,
            color: isHighRisk ? '#FB7185' : '#34D399',
            mb: 2,
            pr: 3,
          }}
        >
          {isHighRisk ? '⚠️ High Churn Risk' : '✅ Low Churn Risk'}
        </Typography>

        <Box sx={{ position: 'relative', display: 'inline-block', mb: 2 }}>
          <ResponsiveContainer width={180} height={180}>
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                innerRadius={55}
                outerRadius={75}
                dataKey="value"
                strokeWidth={0}
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
          
          <Box
            sx={{
              position: 'absolute',
              top: '50%',
              left: '50%',
              transform: 'translate(-50%, -50%)',
            }}
          >
            <Typography 
              variant="h4" 
              sx={{ 
                fontWeight: 800,
                color: isHighRisk ? '#FB7185' : '#34D399',
              }}
            >
              {probability.toFixed(0)}%
            </Typography>
          </Box>
        </Box>

        <Typography 
          variant="body2" 
          sx={{ color: 'rgba(248, 250, 252, 0.7)', mb: 2 }}
        >
          Churn Probability
        </Typography>

        <Box sx={{ mb: 2, px: 2 }}>
          <LinearProgress
            variant="determinate"
            value={probability}
            sx={{
              height: 12,
              borderRadius: 6,
              backgroundColor: 'rgba(71, 85, 105, 0.3)',
              '& .MuiLinearProgress-bar': {
                borderRadius: 6,
                background: isHighRisk ? '#FB7185' : '#34D399',
              },
            }}
          />
        </Box>

        <Chip 
          label={`Confidence: ${confidence}`}
          size="small"
          sx={{
            fontSize: '0.8rem',
            fontWeight: 600,
            background: 'rgba(56, 189, 248, 0.15)',
            border: '1px solid rgba(56, 189, 248, 0.3)',
            color: '#F8FAFC',
            mb: 2,
          }}
        />

        <Box 
          sx={{
            p: 2,
            background: 'rgba(15, 23, 42, 0.5)',
            borderRadius: 2,
            border: '1px solid rgba(248, 250, 252, 0.08)',
          }}
        >
          <Typography 
            variant="subtitle2" 
            sx={{ color: '#F8FAFC', fontWeight: 600, mb: 0.5 }}
          >
            💡 Recommendation
          </Typography>
          <Typography 
            variant="body2" 
            sx={{ color: 'rgba(248, 250, 252, 0.7)', lineHeight: 1.5 }}
          >
            {recommendation}
          </Typography>
        </Box>
      </Box>

      {/* Reset Button */}
      <Button
        onClick={onReset}
        variant="outlined"
        fullWidth
        sx={{
          mt: 2,
          py: 1,
          color: '#38BDF8',
          borderColor: 'rgba(56, 189, 248, 0.3)',
          backgroundColor: 'rgba(56, 189, 248, 0.05)',
          fontWeight: 600,
          '&:hover': {
            borderColor: '#38BDF8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
          },
        }}
      >
        🔄 New Prediction
      </Button>
    </Paper>
  );
};

export default ResultDisplay;