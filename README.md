# Financial Analyzer Agent

Agente de IA que analiza estados financieros y genera memos ejecutivos automaticamente.

![Demo](demo/Animation.gif)

## Que hace

- Calcula ratios financieros: margen bruto, liquidez, endeudamiento
- Detecta alertas y fortalezas automaticamente
- Genera memo ejecutivo con semaforo de riesgo VERDE/AMARILLO/ROJO
- Dashboard interactivo con 1 prueba gratuita diaria

## Stack

Claude API · Python · Streamlit · Tool Use · Agentic Loop

## Correr localmente

```bash
git clone https://github.com/lcarrenoy/financial-analyzer
cd financial-analyzer
uv sync
cp .env.example .env
# Agregar tu ANTHROPIC_API_KEY en .env
uv run streamlit run src/dashboard.py
```

## Experiencia real

Basado en mi experiencia como Business Controller en YUMMY (YC S21)
controlando $7.2M en operaciones anuales de 10 Dark Stores.

## Autor

Luis Carreno · LinkedIn: linkedin.com/in/luis-alberto-carreno

