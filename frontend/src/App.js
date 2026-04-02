import React, { useState } from 'react';
import { Container, Typography, Box } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import PredictionForm from './components/PredictionForm';
import ResultDisplay from './components/ResultDisplay';
import theme from './theme';
import './index.css';

function App() {
  const [prediction, setPrediction] = useState(null);

  const handleReset = () => {
    setPrediction(null);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />

      <Container maxWidth="xl" sx={{ py: 2, px: 3 }}>
        <Box textAlign="center" mb={3}>
          <Typography 
            variant="h4" 
            sx={{ 
              color: '#F8FAFC', 
              mb: 0.5,
              fontWeight: 800,
            }}
          >
            🎯 Customer Churn Predictor
          </Typography>
          <Typography 
            variant="body2" 
            sx={{ color: 'rgba(248, 250, 252, 0.6)' }}
          >
            ML-powered insights for proactive retention
          </Typography>
        </Box>

        {/* Side-by-Side Layout */}
        <Box
          sx={{
            display: 'flex',
            flexDirection: { xs: 'column', md: 'row' },
            gap: 3,
            alignItems: prediction ? 'stretch' : 'flex-start',
            justifyContent: 'center',
          }}
        >
          {/* Left Side - Form */}
          <Box
            sx={{
              flex: prediction ? '0 0 58%' : '0 0 100%',
              maxWidth: prediction ? '58%' : '100%',
              width: '100%',
              transition: 'all 0.5s ease',
              '@media (max-width: 900px)': {
                flex: '0 0 100%',
                maxWidth: '100%',
              },
            }}
          >
            <PredictionForm onPredictionComplete={setPrediction} />
          </Box>

          {/* Right Side - Result */}
          {prediction && (
            <Box
              sx={{
                flex: '0 0 40%',
                maxWidth: '40%',
                width: '100%',
                animation: 'slideIn 0.5s ease',
                '@keyframes slideIn': {
                  from: { opacity: 0, transform: 'translateX(30px)' },
                  to: { opacity: 1, transform: 'translateX(0)' },
                },
                '@media (max-width: 900px)': {
                  flex: '0 0 100%',
                  maxWidth: '100%',
                },
              }}
            >
              <ResultDisplay prediction={prediction} onReset={handleReset} />
            </Box>
          )}
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;