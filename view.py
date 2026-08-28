"""Локальный просмотр деталей в OCP CAD Viewer (VS Code).

Запуск с параметрами:
    python view.py bracket 80 50 10 15     # w h t hole_d
    python view.py box 40 30 5             # w h t
Без аргументов — покажет оба образца (box + bracket).

Требует: pip install ocp-vscode  (пакет вьювера для скриптов),
либо просто открой сгенерированный .step в панели OCP CAD Viewer.
"""

import sys

import cad_builder

SAMPLES = {
    "box": {"w": 40, "h": 30, "t": 5},
    "bracket": {"w": 40, "h": 30, "t": 5, "hole_d": 8},
    "star": {"points": 5, "r_out": 40, "r_in": 16, "t": 5},
}

PARAM_KEYS = {
    "box": ["w", "h", "t"],
    "bracket": ["w", "h", "t", "hole_d"],
    "star": ["points", "r_out", "r_in", "t"],
}


def parse_args(argv):
    """Возвращает {part: params} либо None (показать образцы)."""
    if len(argv) < 2:
        return None
    part = argv[1]
    if part not in PARAM_KEYS:
        raise SystemExit(f"неизвестная деталь: {part} (допустимо: box, bracket)")
    keys = PARAM_KEYS[part]
    raw = argv[2:]
    if len(raw) < len(keys):
        raise SystemExit(f"{part} требует параметры: {' '.join(keys)}")
    nums = [float(x) for x in raw[: len(keys)]]
    return {part: dict(zip(keys, nums))}


def main():
    requested = parse_args(sys.argv)
    parts = requested if requested else SAMPLES

    built = {name: cad_builder.build(name, params) for name, params in parts.items()}
    for name, part in built.items():
        print(f"built {name}: {part}")

    try:
        from ocp_vscode import show

        spaced = [p.translate((i * 80, 0, 0)) for i, p in enumerate(built.values())]
        show(spaced)
    except ImportError:
        print("ocp_vscode не установлен — выполни: pip install ocp-vscode")
        print("или сгенерируй .step через API и открой файл в панели OCP CAD Viewer.")


if __name__ == "__main__":
    main()
