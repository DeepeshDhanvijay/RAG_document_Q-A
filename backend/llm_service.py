from groq import Groq
from typing import List, Tuple
from config import config

class LLMService:
    """Handles LLM interactions using Groq"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or config.GROQ_API_KEY
        if not self.api_key:
            raise ValueError("Groq API key is required")
        self.client = Groq(api_key=self.api_key)
        self.model = config.LLM_MODEL
    
    def generate_answer(self, question: str, context_chunks: List[Tuple[str, float, int]]) -> str:
        """Generate an answer using retrieved context chunks"""
        
        # Prepare context from chunks
        context = "\n\n".join([f"[Chunk {idx + 1}]:\n{chunk}" 
                               for chunk, score, idx in context_chunks])
        
        # Construct prompt
        prompt = f"""You are a helpful AI assistant answering questions about a document. 
Use ONLY the information provided in the context below to answer the question. 
If the answer cannot be found in the context, say "I cannot find this information in the provided document."

Context from document:
{context}

Question: {question}

Please provide a clear, concise answer based solely on the context above. If you reference specific information, mention which chunk it came from."""

        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that answers questions based on provided document context. Always cite your sources by mentioning chunk numbers."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,
                max_tokens=1024,
            )
            
            answer = chat_completion.choices[0].message.content
            return answer
            
        except Exception as e:
            raise Exception(f"Error generating answer with LLM: {str(e)}")
    
    def validate_api_key(self) -> bool:
        """Test if the API key is valid"""
        try:
            self.client.chat.completions.create(
                messages=[{"role": "user", "content": "test"}],
                model=self.model,
                max_tokens=5
            )
            return True
        except Exception:
            return False
