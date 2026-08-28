# Parametric Parts API

FastAPI-сервис, который генерирует 3D-детали по параметрам через **CadQuery**
и отдаёт их в формате STEP/STL. Демонстрирует связку Python-бэкенда и
CAD-автоматизации.

## Stack
- FastAPI = REST API
- CadQuery параметрическое 3D-моделирование
- SQLAlchemy + SQLite = история генераций
- Docker = контейнеризация
- pytest + TestClient = тесты

## Установка
```bash
python -m venv .venv && .venv\Scripts\activate      # Windows
pip install -r requirements.txt
```
> CadQuery тянет за собой pythonocc, установка может занять пару минут.
> Python 3.10/3.11 рекомендуется.

## Запуск
```bash
uvicorn main:app --reload --port 8000
# открыть документацию: http://localhost:8000/docs
```
## Модели

```
.venv\Scripts\Activate.ps1
python view.py bracket 80 50 10 15     # пластина 80×50, толщина 10, дырка 15
python view.py box 40 30 5             # просто параллелепипед
python view.py star 5 40 16 5          # звезда: 5 лучей, Rвнеш=40, Rвнутр=16, толщина 5
python view.py                        # все образцы рядом
```

Параметры `star`: `points, r_out, r_in, t` (нужно `0 < r_in < r_out`, `points >= 2`).
## Эндпоинты
| Метод | Путь | Описание |
|-------|------|----------|
| GET  | `/parts`   | список доступных типов деталей |
| POST | `/generate`| генерация детали, возврат файла |
| GET  | `/history` | история генераций из БД |

## Пример запроса
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"part":"bracket","params":{"w":40,"h":30,"t":5,"hole_d":8},"format":"step"}' \
  -o bracket.step
```

Параметры `box`: `w, h, t`.
Параметры `bracket`: `w, h, t, hole_d`.

## Тесты
```bash
pytest -q
```

## Docker
```bash
docker build -t parts-api .
docker run -p 8000:8000 parts-api
```
