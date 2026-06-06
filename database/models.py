from dataclasses import dataclass

@dataclass
class Medicine:
    id: int = None
    name: str = ""
    time: str = ""
    image: str = ""

@dataclass
class Log:
    id: int = None
    timestamp: str = ""
    status: str = ""
    image: str = ""