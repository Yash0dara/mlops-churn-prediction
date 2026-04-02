import { createTheme } from '@mui/material/styles';

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#38BDF8',
      light: '#7DD3FC',
      dark: '#0284C7',
    },
    secondary: {
      main: '#FB7185',
      light: '#FDA4AF',
      dark: '#F43F5E',
    },
    success: {
      main: '#34D399',
      light: '#6EE7B7',
      dark: '#10B981',
    },
    error: {
      main: '#FB7185',
    },
    background: {
      default: '#0F172A',
      paper: 'rgba(30, 41, 59, 0.7)',
    },
    text: {
      primary: '#F8FAFC',
      secondary: 'rgba(248, 250, 252, 0.7)',
    },
  },
  typography: {
    fontFamily: '"Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h3: {
      fontWeight: 800,
      letterSpacing: '-0.02em',
      color: '#F8FAFC',
    },
    h4: {
      fontWeight: 700,
      letterSpacing: '-0.01em',
      color: '#F8FAFC',
    },
    h5: {
      fontWeight: 600,
      color: '#F8FAFC',
    },
    h6: {
      fontWeight: 600,
      color: '#F8FAFC',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          backgroundImage: 'none',
          backgroundColor: 'rgba(30, 41, 59, 0.7)',
          backdropFilter: 'blur(12px) saturate(180%)',
          border: '1px solid rgba(248, 250, 252, 0.1)',
          boxShadow: '0 4px 24px rgba(0, 0, 0, 0.3)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          textTransform: 'none',
          fontWeight: 600,
          fontSize: '1rem',
          padding: '12px 32px',
        },
        contained: {
          background: '#38BDF8',
          color: '#0F172A',
          boxShadow: '0 4px 20px rgba(56, 189, 248, 0.25)',
          '&:hover': {
            background: '#7DD3FC',
            boxShadow: '0 6px 30px rgba(56, 189, 248, 0.35)',
            transform: 'translateY(-2px)',
          },
          transition: 'all 0.3s ease',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            backgroundColor: '#0F172A',
            borderRadius: 10,
            '& fieldset': {
              borderColor: 'rgba(248, 250, 252, 0.15)',
            },
            '&:hover fieldset': {
              borderColor: 'rgba(248, 250, 252, 0.25)',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#38BDF8',
              borderWidth: 2,
            },
          },
          '& .MuiInputLabel-root': {
            color: 'rgba(248, 250, 252, 0.6)',
          },
          '& .MuiOutlinedInput-input': {
            color: '#F8FAFC',
          },
        },
      },
    },
    MuiSelect: {
      styleOverrides: {
        root: {
          backgroundColor: '#0F172A',
          borderRadius: 10,
          '& .MuiOutlinedInput-notchedOutline': {
            borderColor: 'rgba(248, 250, 252, 0.15)',
          },
          '&:hover .MuiOutlinedInput-notchedOutline': {
            borderColor: 'rgba(248, 250, 252, 0.25)',
          },
          '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
            borderColor: '#38BDF8',
            borderWidth: 2,
          },
        },
        icon: {
          color: 'rgba(248, 250, 252, 0.7)',
        },
      },
    },
    MuiMenuItem: {
      styleOverrides: {
        root: {
          color: '#F8FAFC',
          '&:hover': {
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
          },
          '&.Mui-selected': {
            backgroundColor: 'rgba(56, 189, 248, 0.15)',
            '&:hover': {
              backgroundColor: 'rgba(56, 189, 248, 0.2)',
            },
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(56, 189, 248, 0.15)',
          border: '1px solid rgba(56, 189, 248, 0.3)',
          color: '#F8FAFC',
          fontWeight: 600,
        },
      },
    },
  },
});

export default theme;