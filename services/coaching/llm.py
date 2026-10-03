import os
import logging
from services.config.workout_config import PROMPT

logger = logging.getLogger(__name__)


class LLMCoach:
    def __init__(self, groq_client, model=None):
        self.client = groq_client
        self.history = []
        self.system_prompt = PROMPT
        self.model = model or os.environ.get("GROQ_MODEL", "qwen/qwen3.8-27b")

    def give_feedback(self, event, issue):
        try:
            prompt = f"Event: {event}"

            if issue:
                prompt += f" Form Issue: {issue}"

            messages = [
                {"role": "system", "content": self.system_prompt},
                *self.history[-10:],
                {"role": "user", "content": prompt}
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.4,
            )

            text = response.choices[0].message.content.strip()
            
            self.history.append({"role": "assistant", "content": text})

            return text
            
        except Exception as e:
            logger.error(f"Error getting LLM feedback: {str(e)}")
            # Return a fallback response
            return f"Continue with your {event}. Keep your form steady!"
    