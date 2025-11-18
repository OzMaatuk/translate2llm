"""Example usage of the Translate2LLM service."""
import logging
from translate2llm import TranslateLLM
from translate2llm.services.exceptions import TranslationError, LLMError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

def main():
    """Main function demonstrating Translate2LLM usage."""
    try:
        # Initialize the service
        service = TranslateLLM()
        
        # Example text in different languages
        texts = [
            "Hello, how are you today?",  # English
            "¿Cómo estás hoy?",  # Spanish
            "Comment allez-vous aujourd'hui?",  # French
            "Wie geht es dir heute?",  # German
            "今日はお元気ですか？"  # Japanese
        ]
        
        # Process each text
        for text in texts:
            try:
                # Process with translation and LLM
                result = service.process(
                    text,
                    target_lang="en",  # Translate everything to English
                    system_prompt="You are a helpful assistant. Please provide a friendly response."
                )
                
                # Print results
                print("\n" + "="*50)
                print(f"Original text: {result['original_text']}")
                print(f"Detected language: {result['detected_language']}")
                print(f"Translated text: {result['translated_text']}")
                print(f"LLM response: {result['llm_response']}")
                
            except (TranslationError, LLMError) as e:
                logger.error(f"Processing error: {str(e)}")
                continue
            
    except Exception as e:
        logger.error(f"Application error: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    main()