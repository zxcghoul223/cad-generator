"""Локальный просмотр деталей в OCP CAD Viewer (VS Code).

Запуск:
    python view.py
Требует: pip install ocp-vscode  (пакет вьювера для скриптов),
либо просто открой сгенерированный .step в панели OCP CAD Viewer.
"""

import cad_builder

SAMPLES = {
    "box": {"w": 40, "h": 30, "t": 5},
    "bracket": {"w": 40, "h": 30, "t": 5, "hole_d": 8},
}


def main():
    parts = {name: cad_builder.build(name, params) for name, params in SAMPLES.items()}
    for name, part in parts.items():
        print(f"built {name}: {part}")

    try:
        from ocp_vscode import show

        # разносим детали по X, чтобы грани не совпадали (иначе z-fighting)
        spaced = []
        for i, part in enumerate(parts.values()):
            spaced.append(part.translate((i * 80, 0, 0)))
        show(spaced)
    except ImportError:
        print("ocp_vscode не установлен — выполни: pip install ocp-vscode")
        print("или сгенерируй .step через API и открой файл в панели OCP CAD Viewer.")


if __name__ == "__main__":
    main()
