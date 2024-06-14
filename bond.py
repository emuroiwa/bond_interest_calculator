import numpy as np

def calculate_monthly_payment(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / 12
    total_payments = years * 12
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    return monthly_payment

def generate_amortization_schedule(principal, monthly_payment, monthly_interest_rate, months_to_calculate, additional_payment, lump_sum_payment, lump_sum_month):
    remaining_principal = principal
    amortization_schedule = []

    for month in range(1, months_to_calculate + 1):
        if month == lump_sum_month:
            remaining_principal -= lump_sum_payment

        interest_payment = remaining_principal * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        total_principal_payment = principal_payment + additional_payment
        remaining_principal -= total_principal_payment
        if remaining_principal < 0:
            remaining_principal = 0
        
        amortization_schedule.append({
            "Month": month,
            "Monthly Payment": monthly_payment,
            "Additional Payment": additional_payment,
            "Lump Sum Payment": lump_sum_payment if month == lump_sum_month else 0,
            "Interest Payment": interest_payment,
            "Principal Payment": principal_payment,
            "Total Principal Payment": total_principal_payment,
            "Remaining Principal": remaining_principal
        })

        if remaining_principal == 0:
            break

    return amortization_schedule

# Loan details
principal = 1220000  # loan principal
annual_interest_rate = 0.1058  # annual interest rate
years = 20  # loan term in years
additional_payment = 0  # additional payment towards principal each month
lump_sum_payment = 340000  # lump sum payment towards principal
lump_sum_month = 1  # month in which the lump sum payment is made

# Calculate monthly interest rate
monthly_interest_rate = annual_interest_rate / 12

# Calculate monthly payment
monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, years)

print(f"Monthly Payment: ${monthly_payment:.2f}")

# Calculate the breakdown for the first few months
months_to_calculate = 60  # Adjust this to see more months
amortization_schedule = generate_amortization_schedule(principal, monthly_payment, monthly_interest_rate, months_to_calculate, additional_payment, lump_sum_payment, lump_sum_month)

for payment in amortization_schedule:
    print(f"Month: {payment['Month']}, Monthly Payment: ${payment['Monthly Payment']:.2f}, "
          f"Additional Payment: ${payment['Additional Payment']:.2f}, "
          f"Lump Sum Payment: ${payment['Lump Sum Payment']:.2f}, "
          f"Interest Payment: ${payment['Interest Payment']:.2f}, "
          f"Principal Payment: ${payment['Principal Payment']:.2f}, "
          f"Total Principal Payment: ${payment['Total Principal Payment']:.2f}, "
          f"Remaining Principal: ${payment['Remaining Principal']:.2f}")
