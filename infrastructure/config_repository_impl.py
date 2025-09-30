"""
Implementation of configuration repository using JSON file storage.
"""

import json
import os
from typing import Optional
from domain.repositories import ConfigurationRepository
from domain.exceptions import ConfigurationException


class JsonConfigurationRepository(ConfigurationRepository):
    """Configuration repository implementation using JSON file storage."""
    
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def get_download_path(self) -> str:
        """Get default download path."""
        return self.config.get('download_path', 'downloads')
    
    def set_download_path(self, path: str) -> None:
        """Set default download path."""
        if not path or not path.strip():
            raise ConfigurationException("Download path cannot be empty")
        
        self.config['download_path'] = path
        self._save_config()
    
    def get_preferred_format(self) -> Optional[str]:
        """Get preferred format preference."""
        return self.config.get('preferred_format')
    
    def set_preferred_format(self, format_id: str) -> None:
        """Set preferred format preference."""
        if not format_id or not format_id.strip():
            raise ConfigurationException("Format ID cannot be empty")
        
        self.config['preferred_format'] = format_id
        self._save_config()
    
    def get_config(self, key: str, default=None):
        """Get configuration value by key."""
        return self.config.get(key, default)
    
    def set_config(self, key: str, value) -> None:
        """Set configuration value by key."""
        self.config[key] = value
        self._save_config()
    
    def _load_config(self) -> dict:
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                raise ConfigurationException(f"Error loading configuration: {e}")
        else:
            # Return default configuration
            return {
                'download_path': 'downloads',
                'preferred_format': None,
                'ui_theme': 'light',
                'auto_download': False,
                'show_progress': True
            }
    
    def _save_config(self) -> None:
        """Save configuration to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.config_file) if os.path.dirname(self.config_file) else '.', exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except IOError as e:
            raise ConfigurationException(f"Error saving configuration: {e}")
