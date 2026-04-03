"""
FastAPI application for churn prediction
"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware
from .models import (
    CustomerData, PredictionResponse,
    BatchPredictionRequest, BatchPredictionResponse,
    ModelInfo
)
from .predictor import get_predictor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Customer Churn Prediction API",
    description="Predict customer churn using ML model",
    version="3.0",
    docs_url="/docs",
    redoc_url="/redoc"
)
# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Load model at startup
@app.on_event("startup")
async def startup_event():
    """Initialize model when API starts"""
    logger.info("🚀 Starting Churn Prediction API...")
    try:
        get_predictor()
        logger.info("✅ Model loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load model: {e}")
        raise


@app.get("/")
def read_root():
    """Root endpoint - API info"""
    return {
        "name": "Customer Churn Prediction API",
        "version": "3.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "batch_predict": "/predict/batch",
            "model_info": "/model/info",
            "docs": "/docs"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    try:
        predictor = get_predictor()
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "model_loaded": predictor is not None,
            "model_version": predictor.model_info['model_version']
        }
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={"status": "unhealthy", "error": str(e)}
        )


@app.post("/predict", response_model=PredictionResponse)
def predict_churn(customer: CustomerData):
    """
    Predict churn for a single customer
    
    Returns prediction with probability and recommendation
    """
    try:
        logger.info(f"Prediction request received for customer")
        
        predictor = get_predictor()
        result = predictor.predict_single(customer.dict())
        
        logger.info(f"Prediction: {result['will_churn']} (prob: {result['churn_probability']})")
        
        return result
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


@app.post("/predict/batch", response_model=BatchPredictionResponse)
def predict_batch(request: BatchPredictionRequest):
    """
    Predict churn for multiple customers
    
    Returns predictions for all customers
    """
    try:
        logger.info(f"Batch prediction for {len(request.customers)} customers")
        
        predictor = get_predictor()
        predictions = predictor.predict_batch(request.customers)
        
        # Count predicted churners
        churn_count = sum(1 for p in predictions if p['will_churn'] == 'Yes')
        
        logger.info(f"Batch complete: {churn_count}/{len(predictions)} predicted to churn")
        
        return {
            "predictions": predictions,
            "total_customers": len(predictions),
            "predicted_to_churn": churn_count
        }
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Batch prediction failed: {str(e)}")


@app.get("/model/info", response_model=ModelInfo)
def get_model_info():
    """
    Get model metadata and performance metrics
    """
    try:
        predictor = get_predictor()
        return predictor.get_model_info()
    
    except Exception as e:
        logger.error(f"Error getting model info: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)