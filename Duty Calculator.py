import pandas as pd
import re

df = pd.read_csv("htsdata.csv")

def parse_duty(duty_str, unit_weight=None, quantity=None, cif=1):
    if pd.isna(duty_str): return 0.0
    duty_str = duty_str.strip().lower()
    if "free" in duty_str: return 0.0

    if "%" in duty_str:
        return float(re.search(r"([\d.]+)%", duty_str).group(1)) / 100
    if "¢/kg" in duty_str and unit_weight:
        cents = float(re.search(r"([\d.]+)", duty_str).group(1))
        return (cents * unit_weight) / (100 * cif)
    if "$" in duty_str and "/unit" in duty_str and quantity:
        dollars = float(re.search(r"\$([\d.]+)", duty_str).group(1))
        return (dollars * quantity) / cif
    return 0.0

def calculate_duty(hts_code, product_cost, freight, insurance, weight, quantity):
    cif = product_cost + freight + insurance
    row = df[df["HTS Number"].astype(str).str.startswith(hts_code[:4])].head(1)

    duties = {}
    for col in ["General Rate of Duty", "Special Rate of Duty", "Column 2 Rate of Duty"]:
        rate = parse_duty(row[col].values[0], weight, quantity, cif)
        duties[col] = round(rate * cif, 2)
    return duties
