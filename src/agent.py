import os
import json
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

tools = [
    {
        "name": "calcular_ratios_financieros",
        "description": "Calcula ratios financieros clave",
        "input_schema": {
            "type": "object",
            "properties": {
                "ingresos":          {"type": "number"},
                "costo_ventas":      {"type": "number"},
                "gastos_operativos": {"type": "number"},
                "activo_total":      {"type": "number"},
                "pasivo_total":      {"type": "number"},
                "activo_corriente":  {"type": "number"},
                "pasivo_corriente":  {"type": "number"}
            },
            "required": ["ingresos", "costo_ventas", "gastos_operativos"]
        }
    },
    {
        "name": "detectar_alertas",
        "description": "Detecta alertas en los datos financieros",
        "input_schema": {
            "type": "object",
            "properties": {
                "margen_bruto":   {"type": "number"},
                "margen_neto":    {"type": "number"},
                "ratio_liquidez": {"type": "number"},
                "ratio_deuda":    {"type": "number"}
            },
            "required": ["margen_bruto", "margen_neto"]
        }
    },
    {
        "name": "generar_recomendaciones",
        "description": "Genera recomendaciones estrategicas",
        "input_schema": {
            "type": "object",
            "properties": {
                "alertas":    {"type": "array", "items": {"type": "string"}},
                "fortalezas": {"type": "array", "items": {"type": "string"}},
                "industria":  {"type": "string"}
            },
            "required": ["alertas", "fortalezas"]
        }
    }
]

def calcular_ratios_financieros(ingresos, costo_ventas, gastos_operativos,
                                 activo_total=None, pasivo_total=None,
                                 activo_corriente=None, pasivo_corriente=None):
    utilidad_bruta     = ingresos - costo_ventas
    utilidad_operativa = utilidad_bruta - gastos_operativos
    resultado = {
        "utilidad_bruta":     round(utilidad_bruta, 2),
        "utilidad_operativa": round(utilidad_operativa, 2),
        "margen_bruto":       round((utilidad_bruta / ingresos) * 100, 2),
        "margen_operativo":   round((utilidad_operativa / ingresos) * 100, 2),
    }
    if activo_total and pasivo_total:
        resultado["ratio_deuda"] = round((pasivo_total / activo_total) * 100, 2)
        resultado["patrimonio"]  = round(activo_total - pasivo_total, 2)
    if activo_corriente and pasivo_corriente:
        resultado["ratio_liquidez"] = round(activo_corriente / pasivo_corriente, 2)
    return resultado

def detectar_alertas(margen_bruto, margen_neto, ratio_liquidez=None, ratio_deuda=None):
    alertas    = []
    fortalezas = []
    if margen_bruto < 20:
        alertas.append(f"Margen bruto bajo ({margen_bruto}%)")
    else:
        fortalezas.append(f"Margen bruto solido ({margen_bruto}%)")
    if margen_neto < 5:
        alertas.append(f"Margen neto bajo ({margen_neto}%)")
    else:
        fortalezas.append(f"Margen neto saludable ({margen_neto}%)")
    if ratio_liquidez:
        if ratio_liquidez < 1:
            alertas.append(f"Liquidez critica ({ratio_liquidez}) - riesgo insolvencia")
        elif ratio_liquidez > 2:
            fortalezas.append(f"Buena liquidez ({ratio_liquidez})")
    if ratio_deuda:
        if ratio_deuda > 70:
            alertas.append(f"Alto endeudamiento ({ratio_deuda}%) - riesgo elevado")
        elif ratio_deuda < 40:
            fortalezas.append(f"Bajo endeudamiento ({ratio_deuda}%)")
    return {"alertas": alertas, "fortalezas": fortalezas}

def generar_recomendaciones(alertas, fortalezas, industria="general"):
    prioridad_alta  = [a for a in alertas if "riesgo" in a.lower() or "critica" in a.lower()]
    prioridad_media = [a for a in alertas if a not in prioridad_alta]
    return {
        "total_alertas":    len(alertas),
        "total_fortalezas": len(fortalezas),
        "prioridad_alta":   prioridad_alta,
        "prioridad_media":  prioridad_media,
        "fortalezas":       fortalezas,
        "semaforo":         "ROJO" if prioridad_alta else "AMARILLO" if prioridad_media else "VERDE"
    }

def ejecutar_herramienta(nombre, argumentos):
    if nombre == "calcular_ratios_financieros":
        return calcular_ratios_financieros(**argumentos)
    elif nombre == "detectar_alertas":
        return detectar_alertas(**argumentos)
    elif nombre == "generar_recomendaciones":
        return generar_recomendaciones(**argumentos)
    return {"error": f"Herramienta desconocida: {nombre}"}

def analizar_empresa(datos_empresa, verbose=True):
    messages  = [{"role": "user", "content": datos_empresa}]
    iteracion = 0
    system = """Eres experto en analisis financiero y control de gestion.
Pasos obligatorios:
1. Usa calcular_ratios_financieros con los datos recibidos
2. Usa detectar_alertas con los ratios calculados
3. Usa generar_recomendaciones con las alertas y fortalezas
4. Redacta memo ejecutivo profesional con semaforo VERDE/AMARILLO/ROJO"""

    while True:
        iteracion += 1
        if verbose:
            print(f"\n--- Iteracion {iteracion} ---")

        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=4096,
            system=system,
            tools=tools,
            messages=messages
        )

        if verbose:
            print(f"stop_reason: {response.stop_reason}")

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            return next((b.text for b in response.content if hasattr(b, "text")), "")

        if response.stop_reason == "tool_use":
            tool_results = []
            for bloque in response.content:
                if bloque.type != "tool_use":
                    continue
                if verbose:
                    print(f"Herramienta: {bloque.name}")
                resultado = ejecutar_herramienta(bloque.name, bloque.input)
                if verbose:
                    print(f"Resultado: {json.dumps(resultado, ensure_ascii=False)}")
                tool_results.append({
                    "type":        "tool_result",
                    "tool_use_id": bloque.id,
                    "content":     json.dumps(resultado, ensure_ascii=False)
                })
            messages.append({"role": "user", "content": tool_results})

        if iteracion > 10:
            break

    return "El agente no pudo completar el analisis."

if __name__ == "__main__":
    datos = """
    Analiza TechStart SAC (tecnologia, Q1 2026):
    Ingresos: 850000
    Costo de ventas: 420000
    Gastos operativos: 310000
    Activo total: 1200000
    Pasivo total: 890000
    Activo corriente: 280000
    Pasivo corriente: 310000
    Genera memo ejecutivo completo con semaforo de riesgo.
    """
    print("\n" + "="*50)
    print("FINANCIAL ANALYZER AGENT")
    print("="*50)
    resultado = analizar_empresa(datos)
    print("\n" + "="*50)
    print("MEMO EJECUTIVO")
    print("="*50)
    print(resultado)
