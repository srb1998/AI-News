"""
=============================================================================
AI News Channel - Configuration Settings
=============================================================================
"""

import os
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv


load_dotenv()

@dataclass
class APIConfig:
    """Configuration for all API keys and external services"""
    
    # LLM APIs - Choose based on budget and quality needs
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")  # FREE tier available
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")  # FREE tier available
    
    # News APIs
    NEWSAPI_KEY: str = os.getenv("NEWSAPI_KEY", "")  # FREE: 1000 requests/day
    GNEWSAPI_KEY: str = os.getenv("GNEWSAPI_KEY", "")  # FREE: 1000 requests/day
    SERPER_API_KEY: str = os.getenv("SERPER_API_KEY", "")  # Google search
    
    # AI Services (for future use)
    ELEVENLABS_API_KEY: str = os.getenv("ELEVENLABS_API_KEY", "")  # Voice
    DID_API_KEY: str = os.getenv("DID_API_KEY", "")  # AI Avatar

@dataclass
class LLMConfig:
    """Configuration for Language Models"""
    
    # Default models - optimized for cost vs quality
    DEFAULT_MODEL: str = "llama3-8b-8192"  # Groq free tier
    MANAGER_MODEL: str = "gpt-4-turbo-preview"  # More powerful for manager
    FALLBACK_MODEL: str = "llama3"  # Local Ollama fallback

    # Model parameters
    TEMPERATURE: float = 0.1  # Low temperature for factual news
    MAX_TOKENS: int = 4096

    @property
    def available_models(self) -> Dict[str, str]:
        """Return available models based on API keys"""
        models = {}
        
        if APIConfig.GROQ_API_KEY:
            models.update({
                "groq_llama3": "llama3-8b-8192",
                "groq_mixtral": "mixtral-8x7b-32768",
                "groq_gemma": "gemma-7b-it"
            })
        
        if APIConfig.OPENAI_API_KEY:
            models.update({
                "openai_gpt35": "gpt-3.5-turbo",
                "openai_gpt4": "gpt-4-turbo-preview"
            })
        
        return models

@dataclass
class NewsSourceConfig:
    """Configuration for news sources and RSS feeds"""
    
    # RSS Feeds - Completely FREE and reliable
    RSS_FEEDS: List[Dict] = None
    
    def __post_init__(self):
        if self.RSS_FEEDS is None:
            self.RSS_FEEDS = [
                {
                    "name": "BBC News",
                    "url": "http://feeds.bbci.co.uk/news/rss.xml",
                    "category": "general",
                    "priority": "high",
                    "country": "international"
                },
                {
                    "name": "CNN International",
                    "url": "http://rss.cnn.com/rss/edition.rss",
                    "category": "general",
                    "priority": "high",
                    "country": "international"
                },
                {
                    "name": "Reuters Top News",
                    "url": "https://feeds.reuters.com/reuters/topNews",
                    "category": "general",
                    "priority": "high",
                    "country": "international"
                },
                {
                    "name": "Times of India",
                    "url": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
                    "category": "general",
                    "priority": "high",
                    "country": "india"
                },
                {
                    "name": "The Hindu",
                    "url": "https://www.thehindu.com/news/national/feeder/default.rss",
                    "category": "general",
                    "priority": "medium",
                    "country": "india"
                },
                {
                    "name": "TechCrunch",
                    "url": "https://feeds.feedburner.com/TechCrunch/",
                    "category": "technology",
                    "priority": "medium",
                    "country": "international"
                },
                {
                    "name": "Economic Times",
                    "url": "https://economictimes.indiatimes.com/rssfeedsdefault.cms",
                    "category": "business",
                    "priority": "medium",
                    "country": "india"
                }
            ]
    
    # Collection settings
    MAX_ARTICLES_PER_SOURCE: int = 15
    HOURS_LOOKBACK: int = 24
    MIN_ARTICLE_LENGTH: int = 100
    
    # Content filtering
    BLOCKED_KEYWORDS: List[str] = None
    REQUIRED_KEYWORDS: List[str] = None
    
    def __post_init__(self):
        if self.BLOCKED_KEYWORDS is None:
            self.BLOCKED_KEYWORDS = [
                "adult content", "explicit", "nsfw", 
                # "gambling", "cryptocurrency scam"
            ]

@dataclass
class StorageConfig:
    """Configuration for data storage and file management"""
    
    # Base storage paths
    BASE_PATH: str = "storage/"
    ARTICLES_PATH: str = "storage/articles/"
    REPORTS_PATH: str = "storage/reports/"
    IMAGES_PATH: str = "storage/images/"
    VIDEOS_PATH: str = "storage/videos/"
    SOCIAL_CONTENT_PATH: str = "storage/social_content/"
    
    # File management
    MAX_FILES_PER_FOLDER: int = 1000
    AUTO_CLEANUP_DAYS: int = 30
    BACKUP_ENABLED: bool = True
    
    def ensure_directories(self):
        """Create all necessary directories"""
        import os
        directories = [
            self.BASE_PATH, self.ARTICLES_PATH, self.REPORTS_PATH,
            self.IMAGES_PATH, self.VIDEOS_PATH, self.SOCIAL_CONTENT_PATH
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"📁 Directory ready: {directory}")

@dataclass
class WorkflowConfig:
    """Configuration for workflow scheduling and execution"""
    
    # Timing settings
    DAILY_RUN_TIME: str = "08:00"  # 8 AM daily news
    BREAKING_NEWS_CHECK_INTERVAL: int = 30  # Minutes
    SOCIAL_MEDIA_POST_TIMES: List[str] = None
    
    def __post_init__(self):
        if self.SOCIAL_MEDIA_POST_TIMES is None:
            self.SOCIAL_MEDIA_POST_TIMES = [
                "09:00", "13:00", "17:00", "21:00"  # 4 times daily
            ]
    
    # Quality thresholds
    MIN_ARTICLES_FOR_DAILY_NEWS: int = 10
    MIN_IMPORTANCE_SCORE: float = 0.6
    MAX_PROCESSING_TIME_MINUTES: int = 30
    
    # Content limits
    DAILY_NEWS_ARTICLE_LIMIT: int = 50
    BREAKING_NEWS_ARTICLE_LIMIT: int = 10
    SOCIAL_MEDIA_POSTS_PER_DAY: int = 10

class SystemConfig:
    """Main system configuration that combines all settings"""
    
    def __init__(self):
        self.api = APIConfig()
        self.llm = LLMConfig()
        self.news_sources = NewsSourceConfig()
        self.storage = StorageConfig()
        self.workflow = WorkflowConfig()
        
        # Initialize storage directories
        self.storage.ensure_directories()
    
    def validate_setup(self) -> Dict[str, bool]:
        """Validate system configuration and return status"""
        status = {
            "storage_ready": True,
            "llm_configured": bool(self.api.OPENAI_API_KEY or self.api.GROQ_API_KEY),
            "news_sources_ready": len(self.news_sources.RSS_FEEDS) > 0,
            "newsapi_available": bool(self.api.NEWSAPI_KEY),
            "all_directories_exist": True
        }
        
        # Check if directories exist
        try:
            self.storage.ensure_directories()
        except Exception as e:
            status["storage_ready"] = False
            status["all_directories_exist"] = False
            print(f"❌ Storage setup error: {e}")
        
        return status
    
    def get_optimal_llm(self) -> str:
        """Return the best available LLM based on API keys"""
        if self.api.GROQ_API_KEY:
            return "groq"  # Free tier, fast
        elif self.api.OPENAI_API_KEY:
            return "openai"  # Paid but high quality
        else:
            return "gemini"  # gemini fallback
    
    def print_configuration(self):
        """Print current configuration status"""
        print("🔧 AI News Channel Configuration")
        print("=" * 50)
        
        status = self.validate_setup()
        for key, value in status.items():
            emoji = "✅" if value else "❌"
            print(f"{emoji} {key.replace('_', ' ').title()}: {value}")
        
        print(f"\n🤖 Optimal LLM: {self.get_optimal_llm()}")
        print(f"📰 News Sources: {len(self.news_sources.RSS_FEEDS)}")
        print(f"💾 Storage Path: {self.storage.BASE_PATH}")

# Create global configuration instance
config = SystemConfig()