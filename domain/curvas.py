import numpy as np


def curva_iso834(t: float) -> float:
    """Curva padrão ISO 834."""
    return 20 + 345 * np.log10(8 * t + 1)


def curva_hidrocarboneto(t: float, temp_amb: float = 20.0) -> float:
    """Curva de incêndio por hidrocarbonetos."""
    return temp_amb + 1080 * (
        1
        - 0.33 * np.exp(-0.17 * t)
        - 0.68 * np.exp(-2.50 * t)
    )


def curva_externa(t: float) -> float:
    """Curva de incêndio externa."""
    return 20 + 660 * (
        1
        - 0.687 * np.exp(-0.32 * t)
        - 0.313 * np.exp(-3.8 * t)
    )


def curva_rws(t: float) -> float:
    """Curva RWS (túneis)."""
    tempo_pts = [0, 5, 30, 60, 180]
    temp_pts = [20, 1140, 1300, 1350, 1200]

    return float(np.interp(t, tempo_pts, temp_pts))

