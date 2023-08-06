from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from mashumaro import DataClassDictMixin


@dataclass
class Configuration(DataClassDictMixin):
    profiles: Optional[List[str]] = None
    beans: Optional[Dict[str, Any]] = None
