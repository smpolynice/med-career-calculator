
import streamlit as st

def calculate_net_worth(starting_age, training_years, starting_salary, 
                        pslf, loan_balance, loan_interest, repayment_years, 
                        retirement_age, investment_return, tax_rate):
    age = starting_age
    salary = 0
    savings = 0
    loan = loan_balance

    while age < retirement_age:
        if age < starting_age + training_years:
            salary = 70_000  # average resident/fellow salary
        else:
            salary = starting_salary

        take_home = salary * (1 - tax_rate)
        investable = take_home * 0.20  # assume 20% saved and invested

        if pslf and age >= starting_age + training_years and age < starting_age + training_years + 10:
            # minimal IDR payments during PSLF window
            loan_payment = 5000 if salary > 70_000 else 0
        else:
            # aggressive repayment
            loan_payment = min(loan, (loan_balance / repayment_years) + (loan * loan_interest))

        # Update loan and savings
        loan = max(0, loan * (1 + loan_interest) - loan_payment)
        savings = savings * (1 + investment_return) + investable
        age += 1

    return round(savings / 1_000_000, 2)  # in millions

st.title("💼 Career Path Net Worth Calculator")

st.sidebar.header("🔧 Customize Your Inputs")
starting_age = st.sidebar.number_input("Starting Age", 30, 40, 32)
retirement_age = st.sidebar.number_input("Retirement Age", 55, 70, 60)

loan_balance = st.sidebar.number_input("Loan Balance ($)", 0, 1_000_000, 400_000, step=10_000)
loan_interest = st.sidebar.slider("Loan Interest Rate", 0.01, 0.10, 0.06)

repayment_years = st.sidebar.slider("Aggressive Repayment Term (Years)", 5, 25, 10)
investment_return = st.sidebar.slider("Investment Return", 0.03, 0.10, 0.07)
tax_rate = st.sidebar.slider("Effective Tax Rate", 0.20, 0.40, 0.30)

st.header("📊 Net Worth at Retirement")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Anesthesiology")
    anes_salary = st.number_input("Anes Attending Salary", 300_000, 600_000, 450_000, step=10_000)
    anes_pslf = st.checkbox("Anes on PSLF (Academic)", value=False)
    anes_worth = calculate_net_worth(starting_age, 4, anes_salary, anes_pslf, loan_balance, loan_interest,
                                     repayment_years, retirement_age, investment_return, tax_rate)
    st.success(f"Estimated Net Worth: ${anes_worth}M")

with col2:
    st.subheader("Gastroenterology")
    gi_salary = st.number_input("GI Attending Salary", 350_000, 700_000, 550_000, step=10_000)
    gi_pslf = st.checkbox("GI on PSLF (Academic)", value=False)
    gi_worth = calculate_net_worth(starting_age, 6, gi_salary, gi_pslf, loan_balance, loan_interest,
                                   repayment_years, retirement_age, investment_return, tax_rate)
    st.success(f"Estimated Net Worth: ${gi_worth}M")

st.caption("This is a simple tool. Actual financial outcomes may vary based on location, lifestyle, and career changes.")
