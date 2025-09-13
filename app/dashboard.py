# app/dashboard.py

import streamlit as st
import polars as pl
import plotly.express as px

st.set_page_config(page_title="Dashboard PyME", layout="wide")

# Título principal
st.title("📊 Dashboard PyME - Ventas Demo")

# Cargar CSV
df = pl.read_csv("samples/ventas_demo.csv")

# Calcular importe por fila
df = df.with_columns(
    (df["cantidad"] * df["precio"]).alias("importe")
)

# KPIs
total_ventas = df["importe"].sum()
total_transacciones = df.height
total_sucursales = df["sucursal"].n_unique()

col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Ventas", f"${total_ventas:,.2f}")
col2.metric("🧾 Transacciones", total_transacciones)
col3.metric("🏬 Sucursales", total_sucursales)

# Ventas por día
ventas_dia = df.group_by("fecha").agg([
    pl.col("importe").sum().alias("ventas_dia")
])
fig1 = px.bar(ventas_dia.to_pandas(), x="fecha", y="ventas_dia", title="📆 Ventas por Día")
st.plotly_chart(fig1, use_container_width=True)

# Ventas por sucursal
ventas_sucursal = df.group_by("sucursal").agg([
    pl.col("importe").sum().alias("ventas_sucursal")
])
fig2 = px.pie(ventas_sucursal.to_pandas(), values="ventas_sucursal", names="sucursal", title="🏬 Ventas por Sucursal")
st.plotly_chart(fig2, use_container_width=True)



