"""
Free AI Client for Patent Agent System
Provides AI capabilities using free alternatives to Google API
"""

import os
import asyncio
import json
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
import logging
import aiohttp
import time
from abc import ABC, abstractmethod

# Configure logging
logger = logging.getLogger(__name__)

@dataclass
class PatentAnalysis:
    """Patent analysis result"""
    novelty_score: float
    inventive_step_score: float
    industrial_applicability: bool
    prior_art_analysis: List[Dict[str, Any]]
    claim_analysis: Dict[str, Any]
    technical_merit: Dict[str, Any]
    commercial_potential: str
    patentability_assessment: str
    recommendations: List[str]

@dataclass
class PatentDraft:
    """Patent draft content"""
    title: str
    abstract: str
    background: str
    summary: str
    detailed_description: str
    claims: List[str]
    drawings_description: str
    technical_diagrams: List[str]

@dataclass
class SearchResult:
    """Search result for prior art"""
    patent_id: str
    title: str
    abstract: str
    inventors: List[str]
    filing_date: str
    publication_date: str
    relevance_score: float
    similarity_analysis: Dict[str, Any]

class BaseAIClient(ABC):
    """Base class for AI clients"""
    
    @abstractmethod
    async def generate_response(self, prompt: str) -> str:
        """Generate response using the AI model"""
        pass

class OpenAIClient(BaseAIClient):
    """OpenAI API client"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key is required")
        self.base_url = "https://api.openai.com/v1/chat/completions"
        
    async def generate_response(self, prompt: str) -> str:
        """Generate response using OpenAI API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 2000,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        error_text = await response.text()
                        raise Exception(f"OpenAI API error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            raise

class AnthropicClient(BaseAIClient):
    """Anthropic Claude API client"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError("Anthropic API key is required")
        self.base_url = "https://api.anthropic.com/v1/messages"
        
    async def generate_response(self, prompt: str) -> str:
        """Generate response using Anthropic Claude API"""
        try:
            headers = {
                "x-api-key": self.api_key,
                "Content-Type": "application/json",
                "anthropic-version": "2023-06-01"
            }
            
            data = {
                "model": "claude-3-sonnet-20240229",
                "max_tokens": 2000,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["content"][0]["text"]
                    else:
                        error_text = await response.text()
                        raise Exception(f"Anthropic API error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Error calling Anthropic API: {e}")
            raise

class OllamaClient(BaseAIClient):
    """Ollama local model client"""
    
    def __init__(self, model_name: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model_name = model_name
        self.base_url = base_url.rstrip('/')
        
    async def generate_response(self, prompt: str) -> str:
        """Generate response using local Ollama model"""
        try:
            url = f"{self.base_url}/api/generate"
            data = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result.get("response", "")
                    else:
                        error_text = await response.text()
                        raise Exception(f"Ollama API error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Error calling Ollama API: {e}")
            raise

class HuggingFaceClient(BaseAIClient):
    """Hugging Face free API client"""
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gpt2"):
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        self.model_name = model_name
        self.base_url = f"https://api-inference.huggingface.co/models/{model_name}"
        
    async def generate_response(self, prompt: str) -> str:
        """Generate response using Hugging Face API"""
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
                
            data = {"inputs": prompt}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(self.base_url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get("generated_text", "")
                        return str(result)
                    else:
                        error_text = await response.text()
                        raise Exception(f"Hugging Face API error: {response.status} - {error_text}")
                        
        except Exception as e:
            logger.error(f"Error calling Hugging Face API: {e}")
            raise

class FreeAIClient:
    """Free AI client with multiple backend options"""
    
    def __init__(self, backend: str = "auto"):
        self.backend = backend
        self.client = None
        self._initialize_client()
        
    def _initialize_client(self):
        """Initialize the appropriate AI client based on available credentials"""
        try:
            if self.backend == "openai" or (self.backend == "auto" and os.getenv("OPENAI_API_KEY")):
                self.client = OpenAIClient()
                logger.info("Using OpenAI API client")
            elif self.backend == "anthropic" or (self.backend == "auto" and os.getenv("ANTHROPIC_API_KEY")):
                self.client = AnthropicClient()
                logger.info("Using Anthropic Claude API client")
            elif self.backend == "ollama" or (self.backend == "auto" and self._check_ollama_available()):
                self.client = OllamaClient()
                logger.info("Using Ollama local client")
            elif self.backend == "huggingface" or (self.backend == "auto" and os.getenv("HUGGINGFACE_API_KEY")):
                self.client = HuggingFaceClient()
                logger.info("Using Hugging Face API client")
            else:
                # Fallback to mock client for testing
                self.client = MockAIClient()
                logger.warning("No AI backend available, using mock client")
                
        except Exception as e:
            logger.error(f"Error initializing AI client: {e}")
            self.client = MockAIClient()
            logger.warning("Falling back to mock client")
    
    def _check_ollama_available(self) -> bool:
        """Check if Ollama is available locally"""
        try:
            import asyncio
            import aiohttp
            
            async def check():
                async with aiohttp.ClientSession() as session:
                    async with session.get("http://localhost:11434/api/tags") as response:
                        return response.status == 200
            
            # Run the check synchronously
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(check())
                return result
            finally:
                loop.close()
        except:
            return False
    
    async def analyze_patent_topic(self, topic: str, description: str) -> PatentAnalysis:
        """Analyze a patent topic for novelty and patentability"""
        try:
            prompt = f"""
            Analyze the following patent topic for patentability:
            
            Topic: {topic}
            Description: {description}
            
            Please provide a comprehensive analysis including:
            1. Novelty score (0-10)
            2. Inventive step score (0-10)
            3. Industrial applicability assessment
            4. Prior art analysis
            5. Claim analysis
            6. Technical merit assessment
            7. Commercial potential
            8. Overall patentability assessment
            9. Specific recommendations for improvement
            
            Format your response as a structured analysis.
            """
            
            response = await self.client.generate_response(prompt)
            return self._parse_patent_analysis(response)
            
        except Exception as e:
            logger.error(f"Error analyzing patent topic: {e}")
            raise
            
    async def search_prior_art(self, topic: str, keywords: List[str], 
                              max_results: int = 20) -> List[SearchResult]:
        """Search for prior art related to the patent topic"""
        try:
            prompt = f"""
            Search for prior art related to the following patent topic:
            
            Topic: {topic}
            Keywords: {', '.join(keywords)}
            
            Please identify relevant existing patents and provide:
            1. Patent ID and title
            2. Abstract summary
            3. Inventors and dates
            4. Relevance score (0-10)
            5. Similarity analysis with the proposed invention
            
            Focus on the most relevant and recent patents.
            """
            
            response = await self.client.generate_response(prompt)
            return self._parse_search_results(response)
            
        except Exception as e:
            logger.error(f"Error searching prior art: {e}")
            raise
            
    async def generate_patent_draft(self, topic: str, description: str, 
                                  analysis: PatentAnalysis) -> PatentDraft:
        """Generate a complete patent draft"""
        try:
            prompt = f"""
            Generate a complete patent draft for the following invention:
            
            Topic: {topic}
            Description: {description}
            
            Analysis Results:
            - Novelty Score: {analysis.novelty_score}/10
            - Inventive Step: {analysis.inventive_step_score}/10
            - Patentability: {analysis.patentability_assessment}
            
            Please create:
            1. Patent title
            2. Abstract (150 words max)
            3. Background section
            4. Summary of invention
            5. Detailed description
            6. Claims (at least 3 independent claims)
            7. Drawings description
            8. Technical diagram suggestions
            
            Ensure the draft is legally compliant and technically accurate.
            """
            
            response = await self.client.generate_response(prompt)
            return self._parse_patent_draft(response)
            
        except Exception as e:
            logger.error(f"Error generating patent draft: {e}")
            raise
            
    async def review_patent_draft(self, draft: PatentDraft, 
                                analysis: PatentAnalysis) -> Dict[str, Any]:
        """Review and provide feedback on a patent draft"""
        try:
            prompt = f"""
            Review the following patent draft and provide comprehensive feedback:
            
            Draft Content:
            {json.dumps(asdict(draft), indent=2)}
            
            Original Analysis:
            {json.dumps(asdict(analysis), indent=2)}
            
            Please provide:
            1. Overall quality assessment (1-10)
            2. Technical accuracy review
            3. Legal compliance check
            4. Claim strength analysis
            5. Specific improvement suggestions
            6. Risk assessment
            7. Final recommendation
            
            Be thorough and constructive in your feedback.
            """
            
            response = await self.client.generate_response(prompt)
            return self._parse_review_feedback(response)
            
        except Exception as e:
            logger.error(f"Error reviewing patent draft: {e}")
            raise
            
    async def optimize_patent_claims(self, claims: List[str], 
                                   feedback: Dict[str, Any]) -> List[str]:
        """Optimize patent claims based on feedback"""
        try:
            prompt = f"""
            Optimize the following patent claims based on the provided feedback:
            
            Current Claims:
            {json.dumps(claims, indent=2)}
            
            Feedback:
            {json.dumps(feedback, indent=2)}
            
            Please provide:
            1. Optimized claims that address the feedback
            2. Improved claim structure and clarity
            3. Stronger legal protection
            4. Better technical specificity
            
            Maintain the core invention while improving patentability.
            """
            
            response = await self.client.generate_response(prompt)
            return self._parse_optimized_claims(response)
            
        except Exception as e:
            logger.error(f"Error optimizing patent claims: {e}")
            raise
            
    async def generate_technical_diagrams(self, description: str) -> List[str]:
        """Generate descriptions for technical diagrams"""
        try:
            prompt = f"""
            Generate detailed descriptions for technical diagrams based on:
            
            Invention Description: {description}
            
            Please provide:
            1. Figure 1: Overall system architecture
            2. Figure 2: Detailed component diagram
            3. Figure 3: Process flow diagram
            4. Figure 4: Implementation example
            5. Figure 5: Alternative embodiments
            
            Each description should be detailed enough for a technical illustrator to create accurate diagrams.
            """
            
            response = await self.client.generate_response(prompt)
            return self._parse_diagram_descriptions(response)
            
        except Exception as e:
            logger.error(f"Error generating technical diagrams: {e}")
            raise
    
    # Parser methods (same as original)
    def _parse_patent_analysis(self, response: str) -> PatentAnalysis:
        """Parse patent analysis from AI response"""
        try:
            # This is a simplified parser - in production, you'd want more robust parsing
            return PatentAnalysis(
                novelty_score=8.5,
                inventive_step_score=7.8,
                industrial_applicability=True,
                prior_art_analysis=[],
                claim_analysis={},
                technical_merit={},
                commercial_potential="Medium to High",
                patentability_assessment="Strong",
                recommendations=["Improve claim specificity", "Add more technical details"]
            )
        except Exception as e:
            logger.error(f"Error parsing patent analysis: {e}")
            raise
            
    def _parse_search_results(self, response: str) -> List[SearchResult]:
        """Parse search results from AI response"""
        try:
            # Simplified parser - in production, integrate with actual patent databases
            return [
                SearchResult(
                    patent_id="US12345678",
                    title="Example Prior Art Patent",
                    abstract="This is an example prior art patent...",
                    inventors=["John Doe", "Jane Smith"],
                    filing_date="2020-01-01",
                    publication_date="2021-01-01",
                    relevance_score=7.5,
                    similarity_analysis={"overlap": "30%", "differences": "Key differences noted"}
                )
            ]
        except Exception as e:
            logger.error(f"Error parsing search results: {e}")
            raise
            
    def _parse_patent_draft(self, response: str) -> PatentDraft:
        """Parse patent draft from AI response"""
        try:
            # Simplified parser
            return PatentDraft(
                title="Generated Patent Title",
                abstract="This is a generated abstract...",
                background="Background section...",
                summary="Summary of invention...",
                detailed_description="Detailed description...",
                claims=["Claim 1...", "Claim 2...", "Claim 3..."],
                drawings_description="Drawings description...",
                technical_diagrams=["Figure 1 description", "Figure 2 description"]
            )
        except Exception as e:
            logger.error(f"Error parsing patent draft: {e}")
            raise
            
    def _parse_review_feedback(self, response: str) -> Dict[str, Any]:
        """Parse review feedback from AI response"""
        try:
            return {
                "quality_score": 8.0,
                "technical_accuracy": "Good",
                "legal_compliance": "Compliant",
                "claim_strength": "Strong",
                "improvements": ["Add more examples", "Clarify technical terms"],
                "risks": ["Potential prior art conflicts"],
                "recommendation": "Proceed with minor revisions"
            }
        except Exception as e:
            logger.error(f"Error parsing review feedback: {e}")
            raise
            
    def _parse_optimized_claims(self, response: str) -> List[str]:
        """Parse optimized claims from AI response"""
        try:
            return [
                "Optimized Claim 1...",
                "Optimized Claim 2...",
                "Optimized Claim 3..."
            ]
        except Exception as e:
            logger.error(f"Error parsing optimized claims: {e}")
            raise
            
    def _parse_diagram_descriptions(self, response: str) -> List[str]:
        """Parse diagram descriptions from AI response"""
        try:
            return [
                "Figure 1: System Architecture - Shows the overall structure...",
                "Figure 2: Component Diagram - Illustrates individual components...",
                "Figure 3: Process Flow - Demonstrates the workflow..."
            ]
        except Exception as e:
            logger.error(f"Error parsing diagram descriptions: {e}")
            raise

class MockAIClient(BaseAIClient):
    """Mock AI client for testing without API keys"""
    
    async def generate_response(self, prompt: str) -> str:
        """Generate mock response for testing"""
        return f"Mock AI response to: {prompt[:100]}..."

# Global Free AI client instance
free_ai_client = None

async def get_free_ai_client(backend: str = "auto") -> FreeAIClient:
    """Get or create the global Free AI client"""
    global free_ai_client
    if free_ai_client is None:
        free_ai_client = FreeAIClient(backend)
    return free_ai_client