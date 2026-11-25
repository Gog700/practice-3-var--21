import os

SPECS = {
    "load_const": {
        "A": 14, "size": 5, "max_b": (1 << 22) - 1, "max_c": (1 << 7) - 1,
        "shift_b": 4, "shift_c": 26
    },
    "read": {
        "A": 0, "size": 3, "max_b": (1 << 7) - 1, "max_c": (1 << 7) - 1,
        "shift_b": 4, "shift_c": 11
    },
    "write": {
        "A": 4, "size": 5, "max_b": (1 << 7) - 1, "max_c": (1 << 25) - 1,
        "shift_b": 4, "shift_c": 11
    },
    "sqrt": {
        "A": 9, "size": 3, "max_b": (1 << 7) - 1, "max_c": (1 << 7) - 1,
        "shift_b": 4, "shift_c": 11
    }
}


def parse_yaml(filepath: str) -> list:
    commands = []
    current = None
    
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Файл не найден: {filepath}")
        
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("- name:"):
                if current:
                    commands.append(current)
                name = line.split(":", 1)[1].strip()
                current = {"name": name}
            elif line.startswith("b:"):
                current["b"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("c:"):
                current["c"] = int(line.split(":", 1)[1].strip())
                
    if current:
        commands.append(current)
    return commands


def translate_to_ir(commands: list) -> list:
    ir = []
    for cmd in commands:
        name = cmd["name"]
        if name not in SPECS:
            raise ValueError(f"Неизвестная команда: {name}")
            
        spec = SPECS[name]
        b = cmd.get("b", 0)
        c = cmd.get("c", 0)
        
        if b < 0 or b > spec["max_b"]:
            raise ValueError(f"Поле B выходит за границы для {name}")
        if c < 0 or c > spec["max_c"]:
            raise ValueError(f"Поле C выходит за границы для {name}")
            
        ir.append({
            "name": name,
            "A": spec["A"],
            "B": b,
            "C": c,
            "size": spec["size"],
            "shift_b": spec["shift_b"],
            "shift_c": spec["shift_c"]
        })
    return ir


def ir_to_bytes(ir_cmd: dict) -> bytes:
    val = (
        ir_cmd["A"] | 
        (ir_cmd["B"] << ir_cmd["shift_b"]) | 
        (ir_cmd["C"] << ir_cmd["shift_c"])
    )
    return val.to_bytes(ir_cmd["size"], byteorder="little")