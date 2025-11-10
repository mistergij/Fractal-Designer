from dataclasses import dataclass, field

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenu


@dataclass
class Actions:
    menu_dict: dict[str, QMenu] = field(default_factory=dict)
    action_dicts: dict[str, dict[str, QAction]] = field(default_factory=dict)
