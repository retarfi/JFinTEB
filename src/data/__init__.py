from pathlib import Path

BAR_FMT: str = "{l_bar}{bar:10}{r_bar}{bar:-10b}"
P_ROOT: Path = Path(__file__).parents[2]
P_DATA: Path = P_ROOT / "data"
