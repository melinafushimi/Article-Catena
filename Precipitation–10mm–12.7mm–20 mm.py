# --- IMPORTS ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# --- UPLOAD DO EXCEL ---
print("Selecione o arquivo 'Dados chuva - Rio Claro.xlsx' do seu computador:")
uploaded = files.upload()
xls_name = "Dados chuva - Rio Claro.xlsx"

# --- PARÂMETROS ---
SHEET = "Folha1"
START_YEAR, END_YEAR = 1994, 2025
OUTNAME = "monthly_climatology_precip_en.png"

# --- LEITURA ROBUSTA ---
# Algumas planilhas vêm com 11 linhas de cabeçalho; tentamos primeiro com header=11,
# e se falhar, caímos para uma leitura simples com as duas primeiras colunas.
try:
    df = pd.read_excel(xls_name, sheet_name=SHEET, header=11, usecols=[0,1])
except Exception:
    df = pd.read_excel(xls_name, sheet_name=SHEET, usecols=[0,1], header=None)
    df.columns = ["Data", "Precipitação"]

# Padronizar nomes
df.columns = [str(c).strip().lower() for c in df.columns]

# Tentar mapear nomes comuns
col_date = [c for c in df.columns if "data" in c or "date" in c][0]
col_p    = [c for c in df.columns if "prec" in c][0]

# Converter tipos
df[col_date] = pd.to_datetime(df[col_date], errors="coerce")
df[col_p]    = pd.to_numeric(df[col_p], errors="coerce")

# Limpar e filtrar período
df = df.dropna(subset=[col_date, col_p]).sort_values(col_date).reset_index(drop=True)
df = df[(df[col_date].dt.year >= START_YEAR) & (df[col_date].dt.year <= END_YEAR)]

# --- CLIMATOLOGIA MENSAL ---
# 1) soma mensal por ano
df["year"]  = df[col_date].dt.year
df["month"] = df[col_date].dt.month
monthly_totals = df.groupby(["year","month"], as_index=False)[col_p].sum().rename(columns={col_p:"P_month_mm"})

# 2) média dos totais mensais por mês (climatologia)
clim = monthly_totals.groupby("month", as_index=False)["P_month_mm"].mean()

# Garantir meses 1..12 e preencher algum mês faltante com 0 (raro)
clim = clim.set_index("month").reindex(range(1,13)).fillna(0).reset_index()

# --- PLOT ---
plt.figure(figsize=(12,7))
plt.bar(clim["month"], clim["P_month_mm"])
plt.title("Monthly climatological distribution of precipitation (1994–2025)\nRibeirão Jacutinga watershed, SP, Brazil")
plt.xlabel("Month")
plt.ylabel("Average monthly precipitation (mm)")
plt.xticks(range(1,13), ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
plt.grid(True, axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()

# --- SALVAR E BAIXAR ---
plt.savefig(OUTNAME, dpi=600, bbox_inches="tight")
plt.show()
print(f"Saved: {OUTNAME}")
files.download(OUTNAME)
