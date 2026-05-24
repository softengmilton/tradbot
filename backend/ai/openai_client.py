import os
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class OpenAIAnalyzer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = "gpt-4-vision-preview"
        self.chat_model = "gpt-4"
        self.client = None
        
        if self.api_key:
            try:
                import openai
                self.client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                logger.warning(f"Failed to initialize OpenAI client: {e}")
        else:
            logger.warning("OPENAI_API_KEY not configured. AI mode will fail.")

    def analyze_chart(self, image_base64: str, symbol: Optional[str] = None) -> dict:
        """
        Send chart screenshot to OpenAI for analysis

        Args:
            image_base64: Base64 encoded image
            symbol: Trading pair symbol (e.g., BTCUSD)

        Returns:
            AI analysis response
        """
        from ai.prompts import CHART_ANALYSIS_PROMPT
        
        try:
            if not self.client:
                return {
                    "status": "error",
                    "message": "OPENAI_API_KEY not configured"
                }
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": CHART_ANALYSIS_PROMPT.format(symbol=symbol or "Unknown")
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1024,
                temperature=0.7
            )

            content = response.choices[0].message.content
            return {
                "status": "success",
                "analysis": content,
                "tokens_used": response.usage.total_tokens if response.usage else 0
            }

        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return {
                "status": "error",
                "message": str(e)
            }
