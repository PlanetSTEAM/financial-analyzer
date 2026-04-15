import streamlit as st
import datetime
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
from agent import analizar_empresa

st.set_page_config(
    page_title="Financial Analyzer Agent",
    page_icon="📊",
    layout="wide"
)

DEMO_RESULTADO = """
## 🚦 Semaforo de Riesgo: 🔴 ALTO

| Indicador | Valor | Semaforo |
|---|---|---|
| Ingresos Q1 | S/ 850,000 | — |
| Utilidad Bruta | S/ 430,000 | — |
| Margen Bruto | 50.59% | 🟢 Verde |
| Margen Operativo | 14.12% | 🟢 Verde |
| Ratio de Liquidez | 0.90x | 🔴 Rojo |
| Ratio de Endeudamiento | 74.17% | 🔴 Rojo |

### Alertas Criticas
**🔴 Liquidez critica (0.90x)** — Brecha de S/ -30,000. Riesgo de incumplimiento en 30-90 dias.

**🔴 Alto endeudamiento (74.17%)** — Limita acceso a credito y encarece financiamiento futuro.

### Fortalezas
**🟢 Margen bruto solido (50.59%)** — Eficiente gestion del costo del servicio.

**🟢 Margen operativo saludable (14.12%)** — El negocio genera valor operativo real.

### Recomendaciones (0-30 dias)
- Auditar cuentas por cobrar y acelerar cobranzas
- Renegociar plazos con proveedores (30-60 dias adicionales)
- Congelar gastos no esenciales en Q2 2026

*Generado por Financial Analyzer Agent — Powered by Claude AI*
"""

def init_session():
    hoy = datetime.date.today()
    if "fecha" not in st.session_state or st.session_state.fecha != hoy:
        st.session_state.fecha     = hoy
        st.session_state.usos      = 0
        st.session_state.resultado = None
        st.session_state.modo      = None

init_session()

st.title("📊 Financial Analyzer Agent")
st.caption("Powered by Claude AI · Control de Gestion Automatizado")

with st.sidebar:
    st.header("Datos de la Empresa")
    empresa   = st.text_input("Nombre de empresa", "TechStart SAC")
    industria = st.selectbox("Industria", ["Tecnologia", "Retail", "Manufactura", "Servicios", "Fintech"])
    periodo   = st.text_input("Periodo", "Q1 2026")
    st.divider()
    st.subheader("Estado de Resultados")
    ingresos          = st.number_input("Ingresos (S/)",          value=850000,  step=10000)
    costo_ventas      = st.number_input("Costo de ventas (S/)",   value=420000,  step=10000)
    gastos_operativos = st.number_input("Gastos operativos (S/)", value=310000,  step=10000)
    st.subheader("Balance General")
    activo_total     = st.number_input("Activo total (S/)",      value=1200000, step=10000)
    pasivo_total     = st.number_input("Pasivo total (S/)",      value=890000,  step=10000)
    activo_corriente = st.number_input("Activo corriente (S/)",  value=280000,  step=10000)
    pasivo_corriente = st.number_input("Pasivo corriente (S/)",  value=310000,  step=10000)
    st.divider()
    usos_restantes = 1 - st.session_state.usos
    if usos_restantes > 0:
        st.success("Prueba gratuita disponible hoy")
    else:
        st.error("Prueba del dia agotada")

st.subheader("Elige como quieres explorar el agente")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Ver video demo")
    st.caption("Mira el agente en accion sin necesitar cuenta")
    ver_video = st.button("Ver Video", use_container_width=True)

with col2:
    st.markdown("#### Ver resultado demo")
    st.caption("Explora un analisis real pregrabado")
    ver_demo = st.button("Ver Demo", use_container_width=True)

with col3:
    st.markdown("#### Usar con tus datos")
    if usos_restantes > 0:
        st.caption("1 prueba gratuita disponible hoy")
    else:
        st.caption("Prueba del dia agotada — vuelve manana")
    analizar = st.button(
        "Analizar Ahora",
        type="primary",
        use_container_width=True,
        disabled=usos_restantes == 0
    )

st.divider()

if ver_video:
    st.session_state.modo = "video"
if ver_demo:
    st.session_state.modo = "demo"
if analizar:
    st.session_state.modo = "analizar"

if st.session_state.modo == "video":
    st.subheader("Demo en video")
    VIDEO_URL = "https://github.com/lcarrenoy/financial-analyzer/raw/main/demo/demo.mp4"
    try:
        st.video(VIDEO_URL)
    except:
        st.info("Video disponible proximamente. Prueba el Demo o Analiza con tus datos.")

elif st.session_state.modo == "demo":
    st.subheader("Resultado de ejemplo — TechStart SAC Q1 2026")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Utilidad Bruta",     "S/ 430,000")
    c2.metric("Utilidad Operativa", "S/ 120,000")
    c3.metric("Margen Bruto",       "50.59%")
    c4.metric("Margen Operativo",   "14.12%")
    st.divider()
    st.markdown(DEMO_RESULTADO)

elif st.session_state.modo == "analizar":
    if usos_restantes <= 0:
        st.error("Ya usaste la prueba gratuita de hoy. Vuelve manana.")
        st.info("Puedes crear tu propia API key gratis en console.anthropic.com")
    else:
        datos = f"""
        Analiza {empresa} ({industria}, {periodo}):
        Ingresos: {ingresos}
        Costo de ventas: {costo_ventas}
        Gastos operativos: {gastos_operativos}
        Activo total: {activo_total}
        Pasivo total: {pasivo_total}
        Activo corriente: {activo_corriente}
        Pasivo corriente: {pasivo_corriente}
        Genera memo ejecutivo completo con semaforo de riesgo.
        """
        ub = ingresos - costo_ventas
        uo = ub - gastos_operativos
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Utilidad Bruta",     f"S/ {ub:,.0f}")
        c2.metric("Utilidad Operativa", f"S/ {uo:,.0f}")
        c3.metric("Margen Bruto",       f"{round((ub/ingresos)*100,1)}%")
        c4.metric("Margen Operativo",   f"{round((uo/ingresos)*100,1)}%")
        st.divider()
        with st.spinner("El agente esta analizando..."):
            resultado = analizar_empresa(datos, verbose=False)
        st.session_state.usos     += 1
        st.session_state.resultado = resultado
        st.markdown(resultado)
        st.download_button(
            label="Descargar Memo",
            data=resultado,
            file_name=f"memo_{empresa}_{periodo}.md",
            mime="text/markdown"
        )

else:
    st.info("Selecciona una opcion arriba para comenzar.")
