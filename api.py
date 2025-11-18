"""FastAPI REST service for Translate2LLM."""
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
from translate2llm import TranslateLLM
from translate2llm.services.exceptions import TranslationError, LLMError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Translate2LLM API",
    description="REST API for text translation and LLM processing",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize service
service = TranslateLLM()


class TranslateRequest(BaseModel):
    """Request model for translation and LLM processing."""
    text: str = Field(..., description="Text to translate and process")
    target_lang: str = Field(default="en", description="Target language code (e.g., 'en', 'es', 'fr')")
    system_prompt: Optional[str] = Field(
        default="You are a helpful assistant.",
        description="System prompt for the LLM"
    )


class TranslateResponse(BaseModel):
    """Response model for translation and LLM processing."""
    original_text: str
    detected_language: str
    translated_text: str
    llm_response: str
    target_language: str


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Translate2LLM API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/translate", response_model=TranslateResponse)
async def translate(request: TranslateRequest):
    """
    Translate text and process through LLM.
    
    Args:
        request: Translation request with text, target language, and system prompt
        
    Returns:
        Translation and LLM processing results
        
    Raises:
        HTTPException: If translation or LLM processing fails
    """
    try:
        result = service.process(
            text=request.text,
            target_lang=request.target_lang,
            system_prompt=request.system_prompt
        )
        
        return TranslateResponse(**result)
        
    except TranslationError as e:
        logger.error(f"Translation error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Translation failed: {str(e)}")
        
    except LLMError as e:
        logger.error(f"LLM error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {str(e)}")
        
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
