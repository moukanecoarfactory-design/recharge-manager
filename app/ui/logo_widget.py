"""Widget réutilisable pour afficher le logo d'un opérateur."""
from pathlib import Path
from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import (
    QPixmap, QPainter, QPainterPath, QColor, QFont, QBrush, QPen
)

LOGOS_DIR = Path(__file__).resolve().parent.parent.parent / "data" / "logos"


def get_operator_logo(code: str):
    path = LOGOS_DIR / f"{code.lower()}.png"
    return path if path.exists() else None


def get_operator_icon(code: str, size: int = 40) -> QPixmap:
    path = get_operator_logo(code)
    if not path:
        return QPixmap()
    pix = QPixmap(str(path))
    if pix.isNull():
        return QPixmap()
    return pix.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )


def make_circular_pixmap(source_pix: QPixmap, size: int) -> QPixmap:
    """Découpe un QPixmap en cercle SANS couper le contenu."""
    if source_pix.isNull():
        return source_pix

    # Redimensionner en gardant le ratio
    scaled = source_pix.scaled(
        size, size,
        Qt.AspectRatioMode.KeepAspectRatio,
        Qt.TransformationMode.SmoothTransformation
    )

    # Canvas carré transparent
    result = QPixmap(size, size)
    result.fill(Qt.GlobalColor.transparent)

    painter = QPainter(result)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)

    # Clip circulaire
    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)

    # Centrer
    x = (size - scaled.width()) // 2
    y = (size - scaled.height()) // 2
    painter.drawPixmap(x, y, scaled)

    painter.end()
    return result


def make_fallback_logo(letter: str, color: str, size: int) -> QPixmap:
    pix = QPixmap(size, size)
    pix.fill(Qt.GlobalColor.transparent)
    painter = QPainter(pix)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    painter.setBrush(QBrush(QColor(color)))
    painter.setPen(Qt.PenStyle.NoPen)
    painter.drawEllipse(0, 0, size, size)
    painter.setPen(QPen(QColor("#ffffff")))
    font = QFont()
    font.setBold(True)
    font.setPointSize(int(size / 2.2))
    painter.setFont(font)
    painter.drawText(pix.rect(), Qt.AlignmentFlag.AlignCenter, letter.upper())
    painter.end()
    return pix


class OperatorLogo(QLabel):
    """Logo opérateur — 56px par défaut, net et rond."""

    def __init__(self, code: str, name: str = "", color: str = "#0ea5e9",
                 size: int = 56, parent=None):
        super().__init__(parent)
        self.code = code
        self.operator_name = name
        self.color = color
        self.size = size

        self.setFixedSize(size, size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        inner_size = size - 4
        pix = get_operator_icon(code, inner_size * 2)

        if not pix.isNull():
            circular = make_circular_pixmap(pix, inner_size)
            self.setPixmap(circular)
            self.setStyleSheet(f"""
                QLabel {{
                    background-color: #ffffff;
                    border: 2px solid {color};
                    border-radius: {size // 2}px;
                }}
            """)
        else:
            letter = (name[0] if name else code[0]).upper()
            fallback = make_fallback_logo(letter, color, inner_size)
            self.setPixmap(fallback)
            self.setStyleSheet(f"""
                QLabel {{
                    background-color: #ffffff;
                    border: 2px solid {color};
                    border-radius: {size // 2}px;
                }}
            """)