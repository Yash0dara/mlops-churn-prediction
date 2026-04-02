import React, { useState } from 'react';
import {
  TextField, Select, MenuItem, FormControl, InputLabel,
  Button, Paper, Typography, Box
} from '@mui/material';
import { predictChurn } from '../services/api';

const PredictionForm = ({ onPredictionComplete }) => {
  const [formData, setFormData] = useState({
    gender: 'Female',
    SeniorCitizen: 'No',
    Partner: 'Yes',
    Dependents: 'No',
    tenure: 24,
    PhoneService: 'Yes',
    MultipleLines: 'No',
    InternetService: 'Fiber optic',
    OnlineSecurity: 'No',
    OnlineBackup: 'Yes',
    DeviceProtection: 'No',
    TechSupport: 'No',
    StreamingTV: 'Yes',
    StreamingMovies: 'Yes',
    Contract: 'Month-to-month',
    PaperlessBilling: 'Yes',
    PaymentMethod: 'Electronic check',
    MonthlyCharges: 89.85,
    TotalCharges: 2156.40,
  });

  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (event) => {
    setFormData({ ...formData, [field]: event.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const result = await predictChurn(formData);
    setLoading(false);

    if (result.success) {
      onPredictionComplete(result.data);
    } else {
      alert('Error: ' + result.error);
    }
  };

  const SectionTitle = ({ children }) => (
    <Typography 
      sx={{ 
        color: '#38BDF8', 
        fontWeight: 700, 
        mb: 2,
        fontSize: '0.8rem',
        textTransform: 'uppercase',
        letterSpacing: '0.5px',
      }}
    >
      {children}
    </Typography>
  );

  // Reusable row with 2 inputs
  const TwoInputRow = ({ children }) => (
    <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
      {children}
    </Box>
  );

  // Reusable single full-width input row
  const OneInputRow = ({ children }) => (
    <Box sx={{ mb: 2 }}>
      {children}
    </Box>
  );

  return (
    <Paper 
      elevation={0}
      sx={{ 
        p: 3,
        background: 'rgba(30, 41, 59, 0.7)',
        backdropFilter: 'blur(12px) saturate(180%)',
        border: '1px solid rgba(248, 250, 252, 0.1)',
        borderRadius: 3,
        height: '100%',
      }}
    >
      <Typography 
        variant="h6" 
        sx={{ color: '#F8FAFC', fontWeight: 700, mb: 4 }}
      >
        📋 Customer Information
      </Typography>
      
      <form onSubmit={handleSubmit}>
        
        {/* Row 1: Demographics | Contract & Billing */}
        <Box sx={{ display: 'flex', gap: 4, mb: 3 }}>
          
          {/* Left Column: Demographics */}
          <Box sx={{ flex: 1 }}>
            <SectionTitle>👤 Demographics</SectionTitle>
            
            <TwoInputRow>
              <FormControl fullWidth size="small">
                <InputLabel>Gender</InputLabel>
                <Select value={formData.gender} onChange={handleChange('gender')}>
                  <MenuItem value="Male">Male</MenuItem>
                  <MenuItem value="Female">Female</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth size="small">
                <InputLabel>Senior Citizen</InputLabel>
                <Select value={formData.SeniorCitizen} onChange={handleChange('SeniorCitizen')}>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
              </FormControl>
            </TwoInputRow>
            
            <TwoInputRow>
              <FormControl fullWidth size="small">
                <InputLabel>Partner</InputLabel>
                <Select value={formData.Partner} onChange={handleChange('Partner')}>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth size="small">
                <InputLabel>Dependents</InputLabel>
                <Select value={formData.Dependents} onChange={handleChange('Dependents')}>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
              </FormControl>
            </TwoInputRow>
          </Box>

          {/* Right Column: Contract & Billing */}
          <Box sx={{ flex: 1 }}>
            <SectionTitle>📝 Contract & Billing</SectionTitle>
            
            <TwoInputRow>
              <FormControl fullWidth size="small">
                <InputLabel>Contract</InputLabel>
                <Select value={formData.Contract} onChange={handleChange('Contract')}>
                  <MenuItem value="Month-to-month">Monthly</MenuItem>
                  <MenuItem value="One year">1 Year</MenuItem>
                  <MenuItem value="Two year">2 Year</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth size="small">
                <InputLabel>Paperless Billing</InputLabel>
                <Select value={formData.PaperlessBilling} onChange={handleChange('PaperlessBilling')}>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
              </FormControl>
            </TwoInputRow>
            
            <OneInputRow>
              <FormControl fullWidth size="small">
                <InputLabel>Payment Method</InputLabel>
                <Select value={formData.PaymentMethod} onChange={handleChange('PaymentMethod')}>
                  <MenuItem value="Electronic check">Electronic Check</MenuItem>
                  <MenuItem value="Mailed check">Mailed Check</MenuItem>
                  <MenuItem value="Bank transfer (automatic)">Bank Transfer</MenuItem>
                  <MenuItem value="Credit card (automatic)">Credit Card</MenuItem>
                </Select>
              </FormControl>
            </OneInputRow>
          </Box>
        </Box>

        {/* Row 2: Account Information | Phone Services */}
        <Box sx={{ display: 'flex', gap: 6, mb: 4 }}>
          
          {/* Left Column: Account Information */}
          <Box sx={{ flex: 1 }}>
            <SectionTitle>💰 Account Information</SectionTitle>
            
            <TwoInputRow>
              <TextField
                fullWidth size="small"
                label="Tenure (months)"
                type="number"
                value={formData.tenure}
                onChange={handleChange('tenure')}
              />
              
              <TextField
                fullWidth size="small"
                label="Monthly Charges ($)"
                type="number"
                value={formData.MonthlyCharges}
                onChange={handleChange('MonthlyCharges')}
              />
            </TwoInputRow>
            
            <OneInputRow>
              <TextField
                fullWidth size="small"
                label="Total Charges ($)"
                type="number"
                value={formData.TotalCharges}
                onChange={handleChange('TotalCharges')}
              />
            </OneInputRow>
          </Box>

          {/* Right Column: Phone Services */}
          <Box sx={{ flex: 1 }}>
            <SectionTitle>📱 Phone Services</SectionTitle>
            
            <TwoInputRow>
              <FormControl fullWidth size="small">
                <InputLabel>Phone Service</InputLabel>
                <Select value={formData.PhoneService} onChange={handleChange('PhoneService')}>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                </Select>
              </FormControl>
              
              <FormControl fullWidth size="small">
                <InputLabel>Multiple Lines</InputLabel>
                <Select value={formData.MultipleLines} onChange={handleChange('MultipleLines')}>
                  <MenuItem value="Yes">Yes</MenuItem>
                  <MenuItem value="No">No</MenuItem>
                  <MenuItem value="No phone service">N/A</MenuItem>
                </Select>
              </FormControl>
            </TwoInputRow>
          </Box>
        </Box>

        {/* Row 3: Internet Services - All 7 in one row */}
        <Box sx={{ mb: 3 }}>
          <SectionTitle>🌐 Internet Services</SectionTitle>
          
          <Box sx={{ display: 'flex', gap: 2 }}>
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>Internet</InputLabel>
              <Select value={formData.InternetService} onChange={handleChange('InternetService')}>
                <MenuItem value="DSL">DSL</MenuItem>
                <MenuItem value="Fiber optic">Fiber</MenuItem>
                <MenuItem value="No">No</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>Security</InputLabel>
              <Select value={formData.OnlineSecurity} onChange={handleChange('OnlineSecurity')}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
                <MenuItem value="No internet service">N/A</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>Backup</InputLabel>
              <Select value={formData.OnlineBackup} onChange={handleChange('OnlineBackup')}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
                <MenuItem value="No internet service">N/A</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>Protection</InputLabel>
              <Select value={formData.DeviceProtection} onChange={handleChange('DeviceProtection')}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
                <MenuItem value="No internet service">N/A</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>Support</InputLabel>
              <Select value={formData.TechSupport} onChange={handleChange('TechSupport')}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
                <MenuItem value="No internet service">N/A</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>TV</InputLabel>
              <Select value={formData.StreamingTV} onChange={handleChange('StreamingTV')}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
                <MenuItem value="No internet service">N/A</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl sx={{ flex: 1 }} size="small">
              <InputLabel>Movies</InputLabel>
              <Select value={formData.StreamingMovies} onChange={handleChange('StreamingMovies')}>
                <MenuItem value="Yes">Yes</MenuItem>
                <MenuItem value="No">No</MenuItem>
                <MenuItem value="No internet service">N/A</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>

        {/* Submit Button */}
        <Button 
          type="submit" 
          variant="contained" 
          size="large" 
          fullWidth 
          disabled={loading}
          sx={{ py: 1.5, fontWeight: 700 }}
        >
          {loading ? '🔮 Analyzing...' : '🚀 Predict Churn'}
        </Button>
      </form>
    </Paper>
  );
};

export default PredictionForm;