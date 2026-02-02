"""Application settings and configuration management."""

import os
from pathlib import Path
from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field, field_validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Project paths
    BASE_DIR: Path = Path(__file__).parent.parent
    DATA_DIR: Path = BASE_DIR / "data"
    TEMPLATES_DIR: Path = DATA_DIR / "templates"
    AUDIT_LOGS_DIR: Path = DATA_DIR / "audit_logs"
    UPLOADS_DIR: Path = DATA_DIR / "uploads"
    LOGS_DIR: Path = BASE_DIR / "logs"
    
    # LLM Configuration
    LLM_PROVIDER: Literal["openai", "anthropic"] = Field(default="openai")
    OPENAI_API_KEY: str = Field(default="")
    OPENAI_MODEL: str = Field(default="gpt-4-turbo-preview")
    ANTHROPIC_API_KEY: str = Field(default="")
    ANTHROPIC_MODEL: str = Field(default="claude-3-opus-20240229")
    
    # Application Settings
    APP_NAME: str = Field(default="Contract Analysis & Risk Assessment Bot")
    APP_VERSION: str = Field(default="1.0.0")
    ENVIRONMENT: Literal["development", "production"] = Field(default="production")
    
    # Security
    SECRET_KEY: str = Field(default="change-this-in-production")
    ENABLE_AUDIT_LOGS: bool = Field(default=True)
    
    # Language Settings
    DEFAULT_LANGUAGE: str = Field(default="en")
    SUPPORTED_LANGUAGES: list[str] = Field(default=["en", "hi"])
    
    # File Upload Settings
    MAX_UPLOAD_SIZE_MB: int = Field(default=10)
    ALLOWED_EXTENSIONS: list[str] = Field(default=["pdf", "docx", "doc", "txt"])
    
    # Risk Thresholds
    RISK_LOW_THRESHOLD: float = Field(default=0.3)
    RISK_MEDIUM_THRESHOLD: float = Field(default=0.6)
    RISK_HIGH_THRESHOLD: float = Field(default=0.8)
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO")
    LOG_FILE_PATH: str = Field(default="./logs/app.log")
    
    # Contract Types
    CONTRACT_TYPES: list[str] = Field(default=[
        "Employment Agreement",
        "Vendor Contract",
        "Lease Agreement",
        "Partnership Deed",
        "Service Contract",
        "Non-Disclosure Agreement",
        "Consultancy Agreement",
        "Purchase Order"
    ])
    
    # Risk Categories
    RISK_CATEGORIES: list[str] = Field(default=[
        "Penalty Clauses",
        "Indemnity Clauses",
        "Unilateral Termination",
        "Arbitration & Jurisdiction",
        "Auto-Renewal & Lock-in",
        "Non-compete & IP Transfer",
        "Payment Terms",
        "Liability Limitations",
        "Confidentiality",
        "Force Majeure"
    ])
    
    @field_validator("SUPPORTED_LANGUAGES", mode="before")
    @classmethod
    def parse_languages(cls, v):
        """Parse comma-separated language string."""
        if isinstance(v, str):
            return [lang.strip() for lang in v.split(",")]
        return v
    
    @field_validator("ALLOWED_EXTENSIONS", mode="before")
    @classmethod
    def parse_extensions(cls, v):
        """Parse comma-separated extensions string."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def create_directories(self):
        """Create required directories if they don't exist."""
        directories = [
            self.DATA_DIR,
            self.TEMPLATES_DIR,
            self.AUDIT_LOGS_DIR,
            self.UPLOADS_DIR,
            self.LOGS_DIR
        ]
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
            # Create .gitkeep for empty directories
            if directory in [self.UPLOADS_DIR, self.AUDIT_LOGS_DIR]:
                gitkeep = directory / ".gitkeep"
                if not gitkeep.exists():
                    gitkeep.touch()
    
    def get_risk_level(self, score: float) -> str:
        """Get risk level based on score."""
        if score < self.RISK_LOW_THRESHOLD:
            return "Low"
        elif score < self.RISK_MEDIUM_THRESHOLD:
            return "Medium"
        elif score < self.RISK_HIGH_THRESHOLD:
            return "High"
        else:
            return "Critical"
    
    def validate_api_keys(self) -> bool:
        """Validate that required API keys are present."""
        if self.LLM_PROVIDER == "openai":
            return bool(self.OPENAI_API_KEY and self.OPENAI_API_KEY != "")
        elif self.LLM_PROVIDER == "anthropic":
            return bool(self.ANTHROPIC_API_KEY and self.ANTHROPIC_API_KEY != "")
        return False


# Singleton instance
_settings: Settings | None = None


def get_settings() -> Settings:
    """Get application settings singleton."""
    global _settings
    if _settings is None:
        _settings = Settings()
        _settings.create_directories()
    return _settings
