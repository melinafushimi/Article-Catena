# --- IMPORTS ---
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from google.colab import files

# --- UPLOAD ---
print("Selecione o arquivo 'Resumo_erosividade_jacutinga.xlsx' do seu computador:")
uploaded = files.upload()
file_path = "Resumo_erosividade_jacutinga.xlsx"

# --- LEITURA ---
df = pd.read_excel(file_path, sheet_name="resumo_erosividade_jacutinga")

# --- CONVERSÕES ROBUSTAS (remover 'Média' e outros textos) ---
# Forçar numérico; tudo que não for número vira NaN
years = pd.to_numeric(df["ano"], errors="coerce")
R_exp = pd.to_numeric(df["R_exp_MJmm_ha_h_yr"], errors="coerce")
R_quad = pd.to_numeric(df["R_quad_MJmm_ha_h_yr"], errors="coerce")

# Máscara: mantém só linhas com ano e valores numéricos válidos
mask = years.notna() & R_exp.notna() & R_quad.notna()
years = years[mask].astype(int)
R_exp = R_exp[mask]
R_quad = R_quad[mask]

# (opcional) garantir ordenação por ano
order = np.argsort(years.values)
years = years.iloc[order]
R_exp = R_exp.iloc[order]
R_quad = R_quad.iloc[order]

# --- PLOT ---
fig, ax1 = plt.subplots(figsize=(10, 6))

# Eixo esquerdo - linha azul (R Exponential)
color1 = 'tab:blue'
ax1.set_xlabel("Year")
ax1.set_ylabel("R Exponential [MJ·mm·ha⁻¹·h⁻¹·yr⁻¹]", color=color1)
line1, = ax1.plot(years, R_exp, color=color1, marker="o", label="R Exponential (line)")
ax1.tick_params(axis='y', labelcolor=color1)

# Eixo direito - barras vermelhas (R Quadratic)
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel("R Quadratic [MJ·mm·ha⁻¹·h⁻¹·yr⁻¹]", color=color2)
bars = ax2.bar(years, R_quad, color=color2, alpha=0.35, label="R Quadratic (bars)")
ax2.tick_params(axis='y', labelcolor=color2)

# Legenda e título
fig.legend([line1, bars],
           ["R Exponential (line)", "R Quadratic (bars)"],
           loc="lower center", bbox_to_anchor=(0.5, -0.12), ncol=2, frameon=False)

plt.title("Annual time series of rainfall erosivity factor (R)\n"
          "Estimated using exponential (line) and quadratic (bars) equations (1994–2025)")

fig.tight_layout()
plt.grid(True, linestyle="--", alpha=0.5)

# --- SALVAR E BAIXAR ---
output_name = "R_factor_timeseries_en.png"
plt.savefig(output_name, dpi=600, bbox_inches="tight")
plt.show()

print(f"Gráfico salvo como: {output_name}")
files.download(output_name)
