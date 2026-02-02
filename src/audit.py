"""Audit trail management for compliance and tracking."""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional
from config.settings import get_settings


class AuditLogger:
    """Manages audit trail logging for contract analysis activities."""
    
    def __init__(self):
        self.settings = get_settings()
        self.audit_dir = self.settings.AUDIT_LOGS_DIR
        
    def log_activity(
        self,
        activity_type: str,
        details: Dict[str, Any],
        user_id: Optional[str] = None,
        session_id: Optional[str] = None
    ) -> str:
        """
        Log an audit trail entry.
        
        Args:
            activity_type: Type of activity (e.g., 'upload', 'analysis', 'export')
            details: Activity-specific details
            user_id: Optional user identifier
            session_id: Optional session identifier
            
        Returns:
            Audit entry ID
        """
        entry_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        audit_entry = {
            "entry_id": entry_id,
            "timestamp": timestamp,
            "activity_type": activity_type,
            "user_id": user_id or "anonymous",
            "session_id": session_id or "default",
            "details": details,
            "app_version": self.settings.APP_VERSION
        }
        
        # Save to file
        if self.settings.ENABLE_AUDIT_LOGS:
            self._save_entry(audit_entry)
        
        return entry_id
    
    def _save_entry(self, entry: Dict[str, Any]):
        """Save audit entry to file."""
        # Create date-based filename
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"audit_{date_str}.jsonl"
        filepath = self.audit_dir / filename
        
        # Append to JSONL file
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    
    def get_session_history(self, session_id: str) -> list[Dict[str, Any]]:
        """
        Retrieve audit history for a specific session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            List of audit entries
        """
        entries = []
        
        # Search through audit files
        for audit_file in self.audit_dir.glob("audit_*.jsonl"):
            with open(audit_file, "r", encoding="utf-8") as f:
                for line in f:
                    entry = json.loads(line)
                    if entry.get("session_id") == session_id:
                        entries.append(entry)
        
        return sorted(entries, key=lambda x: x["timestamp"])
    
    def log_contract_upload(
        self, 
        filename: str, 
        file_size: int, 
        file_type: str,
        session_id: str
    ) -> str:
        """Log contract file upload."""
        return self.log_activity(
            activity_type="contract_upload",
            details={
                "filename": filename,
                "file_size_bytes": file_size,
                "file_type": file_type
            },
            session_id=session_id
        )
    
    def log_analysis_request(
        self,
        contract_type: str,
        language: str,
        session_id: str
    ) -> str:
        """Log contract analysis request."""
        return self.log_activity(
            activity_type="analysis_request",
            details={
                "contract_type": contract_type,
                "language": language
            },
            session_id=session_id
        )
    
    def log_analysis_completion(
        self,
        session_id: str,
        analysis_results: Dict[str, Any],
        processing_time_seconds: float
    ) -> str:
        """Log contract analysis completion."""
        return self.log_activity(
            activity_type="analysis_completion",
            details={
                "contract_type": analysis_results.get("contract_type"),
                "risk_score": analysis_results.get("overall_risk_score"),
                "clauses_analyzed": len(analysis_results.get("clauses", [])),
                "processing_time_seconds": processing_time_seconds
            },
            session_id=session_id
        )
    
    def log_report_export(
        self,
        report_type: str,
        export_format: str,
        session_id: str
    ) -> str:
        """Log report export."""
        return self.log_activity(
            activity_type="report_export",
            details={
                "report_type": report_type,
                "export_format": export_format
            },
            session_id=session_id
        )
    
    def log_error(
        self,
        error_type: str,
        error_message: str,
        session_id: str,
        stack_trace: Optional[str] = None
    ) -> str:
        """Log error occurrence."""
        return self.log_activity(
            activity_type="error",
            details={
                "error_type": error_type,
                "error_message": error_message,
                "stack_trace": stack_trace
            },
            session_id=session_id
        )
