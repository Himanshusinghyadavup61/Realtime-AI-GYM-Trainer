from io import BytesIO
from gtts import gTTS
import logging

logger = logging.getLogger(__name__)


class TextToSpeech:
    def speak(self, text, lang="en"):
        cleaned = (text or "").strip()

        if not cleaned:
            return None
        
        try:
            buffer = BytesIO()
            
            # Limit text length to avoid API issues
            if len(cleaned) > 1000:
                cleaned = cleaned[:1000] + "..."
            
            gTTS(text=cleaned, lang=lang, slow=False).write_to_fp(buffer)

            buffer.seek(0)
            audio_data = buffer.read()
            
            if not audio_data:
                logger.warning("gTTS returned empty audio data")
                return None
                
            return audio_data
            
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            return None
    