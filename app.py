import streamlit as st
import pandas as pd

st.set_page_config(page_title="Roommate Expense Splitter", page_icon="💰", layout="wide")

st.title("🏠 Smart Roommate Expense Splitter")

st.divider()

# -------------------------
# Roommates
# -------------------------

st.header("1️⃣ Roommates")

num_people = st.number_input("Number of roommates", min_value=1, step=1)

names = []

for i in range(int(num_people)):
    name = st.text_input(f"Roommate {i+1} Name", key=f"name_{i}")
    if name:
        names.append(name)

st.divider()

# -------------------------
# Common Expenses
# -------------------------

st.header("2️⃣ Common Expenses")

common_rows = []

def add_common(expense, amount, payer):
    if amount > 0 and payer != "-- Select Person --":
        common_rows.append({"Person": payer, "Expense": expense, "Amount": amount})

rent = st.number_input("Rent Amount", min_value=0.0)
rent_payer = st.selectbox("Who paid Rent?", ["-- Select Person --"] + names)
add_common("Rent", rent, rent_payer)

maid = st.number_input("Maid Amount", min_value=0.0)
maid_payer = st.selectbox("Who paid Maid?", ["-- Select Person --"] + names)
add_common("Maid", maid, maid_payer)

water = st.number_input("Water Amount", min_value=0.0)
water_payer = st.selectbox("Who paid Water?", ["-- Select Person --"] + names)
add_common("Water", water, water_payer)

garbage = st.number_input("Garbage Amount", min_value=0.0)
garbage_payer = st.selectbox("Who paid Garbage?", ["-- Select Person --"] + names)
add_common("Garbage", garbage, garbage_payer)

# -------------------------
# Electricity
# -------------------------

st.subheader("⚡ Electricity")

prev_unit = st.number_input("Previous Month Meter Reading", min_value=0.0)
current_unit = st.number_input("Current Month Meter Reading", min_value=0.0)

price_per_unit = st.number_input("Price Per Unit (₹)", min_value=0.0)

electricity_payer = st.selectbox(
    "Who paid Electricity?",
    ["-- Select Person --"] + names
)

units_used = max(current_unit - prev_unit, 0)

electricity_amount = units_used * price_per_unit

rounded_electricity = round(electricity_amount)

st.write(f"Units Used = {units_used}")
st.write(f"Electricity Amount = ₹{electricity_amount:.2f}")
st.write(f"Rounded Amount = ₹{rounded_electricity}")

add_common("Electricity", rounded_electricity, electricity_payer)

st.divider()

# -------------------------
# Personal Expenses
# -------------------------

st.header("3️⃣ Personal Expenses")

personal_rows = []

for name in names:

    st.subheader(f"Expenses by {name}")

    food = st.number_input(f"Food by {name}", min_value=0.0, key=f"food_{name}")
    other = st.number_input(f"Other by {name}", min_value=0.0, key=f"other_{name}")

    if food > 0:
        personal_rows.append({"Person": name, "Expense": "Food", "Amount": food})

    if other > 0:
        personal_rows.append({"Person": name, "Expense": "Other", "Amount": other})

st.divider()

# -------------------------
# Calculation
# -------------------------

if st.button("Calculate Split"):

    df_common = pd.DataFrame(common_rows)
    df_personal = pd.DataFrame(personal_rows)

    common_total = df_common["Amount"].sum() if not df_common.empty else 0
    per_person_common = common_total / num_people

    st.header("📊 Common Expense Summary")

    st.write(f"Total Common Expense = ₹{common_total}")
    st.write(f"Each Person Share = ₹{per_person_common:.2f}")

    # personal map
    personal_map = {}

    for person in names:
        personal_map[person] = sum(
            r["Amount"] for r in personal_rows if r["Person"] == person
        )

    df_all = pd.concat([df_common, df_personal], ignore_index=True)
    paid_map = df_all.groupby("Person")["Amount"].sum().to_dict()

    results = []

    for person in names:

        personal_paid = personal_map.get(person, 0)
        should_pay = per_person_common + personal_paid
        paid = paid_map.get(person, 0)

        balance = paid - should_pay

        results.append({
            "Person": person,
            "Paid": paid,
            "Should Pay": should_pay,
            "Balance": balance
        })

    result_df = pd.DataFrame(results)

    st.header("🧾 Per Person Calculation")

    st.dataframe(result_df)

    # -------------------------
    # Settlement
    # -------------------------

    creditors = []
    debtors = []

    for r in results:

        if r["Balance"] > 0:
            creditors.append([r["Person"], r["Balance"]])

        elif r["Balance"] < 0:
            debtors.append([r["Person"], -r["Balance"]])

    settlements = []

    for debtor in debtors:

        d_name = debtor[0]
        d_amt = debtor[1]

        for creditor in creditors:

            c_name = creditor[0]
            c_amt = creditor[1]

            if d_amt == 0:
                break

            pay = min(d_amt, c_amt)

            settlements.append((d_name, c_name, pay))

            debtor[1] -= pay
            creditor[1] -= pay

            d_amt -= pay

    # -------------------------
    # Display Settlement
    # -------------------------

    st.header("💰 Final Settlement")

    transactions = {}

    for d, c, amt in settlements:

        transactions.setdefault(d, {"pay": [], "receive": []})
        transactions.setdefault(c, {"pay": [], "receive": []})

        transactions[d]["pay"].append((c, amt))
        transactions[c]["receive"].append((d, amt))

    for person in names:

        st.subheader(person)

        if person in transactions:

            if transactions[person]["receive"]:
                st.write("Receive From:")
                for p, amt in transactions[person]["receive"]:
                    st.write(f"{p} : ₹{amt:.2f}")

            if transactions[person]["pay"]:
                st.write("Pay To:")
                for p, amt in transactions[person]["pay"]:
                    st.write(f"{p} : ₹{amt:.2f}")

        else:
            st.write("No transactions")

st.divider()

st.caption("Roommate expense manager with electricity unit calculation")