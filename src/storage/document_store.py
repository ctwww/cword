"""
Document Store - Save generated documents
"""

from pathlib import Path
from datetime import datetime
from typing import Optional


class DocumentStore:
    """Store generated documents"""

    def __init__(self, config: dict):
        self.config = config
        self.output_dir = self._get_output_dir()

    def _get_output_dir(self) -> Path:
        """Get output directory path"""
        output_path = self.config.get("directories", {}).get("output", "~/.cword/output")
        path = Path(output_path).expanduser()
        path.mkdir(parents=True, exist_ok=True)
        return path

    def save_document(
        self,
        product_name: str,
        document_type: str,
        content: str,
        format: str = "markdown"
    ) -> Path:
        """Save document to file"""
        # Sanitize product name for filename
        safe_name = product_name.replace(' ', '_').replace('/', '_')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Determine file extension
        ext = "md" if format == "markdown" else "txt"

        # Create filename
        filename = f"{safe_name}_{document_type}_{timestamp}.{ext}"
        file_path = self.output_dir / filename

        # Write content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        return file_path

    def save_prd(self, product_name: str, content: str) -> Path:
        """Save PRD document"""
        return self.save_document(product_name, "PRD", content)

    def save_tech_design(self, product_name: str, content: str) -> Path:
        """Save technical design document"""
        return self.save_document(product_name, "Tech_Design", content)

    def save_decision_history(self, product_name: str, content: str) -> Path:
        """Save decision history"""
        return self.save_document(product_name, "Decision_History", content)

    def get_document_path(self, product_name: str, document_type: str) -> Optional[Path]:
        """Get path to existing document"""
        safe_name = product_name.replace(' ', '_').replace('/', '_')

        # Search for matching files
        pattern = f"{safe_name}_{document_type}_*.*"
        matching_files = list(self.output_dir.glob(pattern))

        if matching_files:
            # Return most recent
            matching_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
            return matching_files[0]

        return None

    def list_documents(self, product_name: str = None) -> list:
        """List all documents or documents for specific product"""
        if product_name:
            safe_name = product_name.replace(' ', '_').replace('/', '_')
            pattern = f"{safe_name}_*.*"
            files = list(self.output_dir.glob(pattern))
        else:
            files = list(self.output_dir.glob("*_*.md"))

        # Sort by modification time
        files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        return files
