import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import math

st.title("Car Payment Calculator")

#Section for User Input
st.write("###Input Data Here")
col1, col2 = st.columns(2)
car_value = col1.number_input("Car Value", min_value=0, value=750000)
deposit = col1.number_input("Your Deposit", min_value=0, max_value=300000)
interest_rate = col2.number_input("Interest Rate %", min_value=0.0, max_value=15.0)
term = col2.number_input("Term in years", min_value=1, max_value=15)

#Calculation of Payments
loan_amount = car_value - deposit
monthly_interest_rate = (interest_rate/100)/12
number_of_payments = term*12
monthly_payment_cost = (
    loan_amount
    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
)

#Section to Display Graph
total_payments = monthly_payment_cost * number_of_payments
total_interes_rate = total_payments - loan_amount

st.write("### Repayments Over Time")
col1, col2, col3 = st.columns(3)
col1.metric(label="Monthly Repayments", value=f"${monthly_payment_cost:,.2f}")
col1.metric(label="Total Repayments", value=f"${total_payments:,.2f}")
col1.metric(label="Total Interest", value=f"${total_interes_rate:,.2f}")

#Creation of Data-Fraem With Payment Schedule
schedule = []
remaining_balance = loan_amount

for i in range(1, number_of_payments +1):
    interest_payment = remaining_balance * monthly_interest_rate
    principal_payment = monthly_payment_cost - interest_payment
    remaining_balance -= principal_payment
    year = math.ceil(i/12) # Calculating The Year Into The Loasn
    schedule.append(
        [
            i,
            monthly_payment_cost,
            interest_payment,
            remaining_balance,
            year
        ]
    )

# Send Data To Panda Data Frame
df = pd.DataFrame(
    schedule, columns=["Month", "Payment", "Principal", "Interest", "Remaining Balance", "Year"],
)

#Display Data-Frame as Graph to User
st.write("### Payment Schedule")
payment_df = df[["Year", "Remaining Balance"]].groupby("Year").min()
st.line_chart(payment_df)
