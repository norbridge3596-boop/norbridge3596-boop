#!/usr/bin/env python3
"""Weekly revenue check for Norbridge Tools."""
import json, requests, sys
from datetime import datetime, timedelta

TOKEN = "zMioZMhKvJPqwP9p2cQwNeRJKwrU7nc3umYf1DrQnEc"

# Check Gumroad sales
r = requests.get("https://api.gumroad.com/v2/sales?access_token=" + TOKEN)
if r.status_code == 200:
    data = r.json()
    sales = data.get('sales', [])
    total = sum(float(s.get('formatted_total_price', '0').replace('$','').replace('A','')) for s in sales)
    count = len(sales)
    print(f"  Gumroad sales: {count} total, ${total:.2f}")
else:
    print(f"  Gumroad API: {r.status_code}")

# Check GitHub Sponsors
print(f"  Checked: {datetime.utcnow().isoformat()}Z")
