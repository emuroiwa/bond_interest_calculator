import numpy as np
from flask import Flask

app = Flask(__name__)
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/data')
def getData():        
    # Loan details
    principal = 1220000  # loan principal
    initial_annual_interest_rate = 0.1058  # initial annual interest rate
    years = 20  # loan term in years
    additional_payment = 0  # additional payment towards principal each month
    lump_sum_payment = 0  # lump sum payment towards principal
    lump_sum_month = 1  # month in which the lump sum payment is made

    # Interest rate changes
    interest_rate_changes = {
        0: 0.1058,
        3: 0.1032, 
    }

    # Calculate the breakdown for the first few months
    months_to_calculate = 240  # Adjust this to see more months
    amortization_schedule = generate_amortization_schedule(principal, initial_annual_interest_rate, years, months_to_calculate, additional_payment, lump_sum_payment, lump_sum_month, interest_rate_changes)

    data = ""
    for payment in amortization_schedule:
            data += f"Month: {payment['Month']}, Monthly Payment: ${payment['Monthly Payment']:.2f}, "
            f"Additional Payment: ${payment['Additional Payment']:.2f}, "
            f"Lump Sum Payment: ${payment['Lump Sum Payment']:.2f}, "
            f"Interest Payment: ${payment['Interest Payment']:.2f}, "
            f"Principal Payment: ${payment['Principal Payment']:.2f}, "
            f"Total Principal Payment: ${payment['Total Principal Payment']:.2f}, "
            f"Interest Percentage: {payment['Percent']:.2f}%, "
            f"Remaining Principal: ${payment['Remaining Principal']:.2f} <br>"
    return data


def calculate_monthly_payment(principal, annual_interest_rate, years):
    monthly_interest_rate = annual_interest_rate / 12
    total_payments = years * 12
    monthly_payment = principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
    return monthly_payment

def get_current_interest_rate(month, interest_rates):
    for start_month, rate in sorted(interest_rates.items(), reverse=True):
        if month >= start_month:
            return rate / 12
    return interest_rates[0] / 12

def generate_amortization_schedule(principal, initial_annual_interest_rate, years, months_to_calculate, additional_payment, lump_sum_payment, lump_sum_month, interest_rate_changes):
    remaining_principal = principal
    amortization_schedule = []
    monthly_payment = calculate_monthly_payment(principal, initial_annual_interest_rate, years)

    for month in range(1, months_to_calculate + 1):
        current_monthly_interest_rate = get_current_interest_rate(month, interest_rate_changes)

        if month == lump_sum_month:
            remaining_principal -= lump_sum_payment

        interest_payment = remaining_principal * current_monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        total_principal_payment = principal_payment + additional_payment
        remaining_principal -= total_principal_payment
        interest_percentage = (interest_payment / monthly_payment) * 100
        if remaining_principal < 0:
            remaining_principal = 0
        
        amortization_schedule.append({
            "Month": month,
            "Monthly Payment": monthly_payment,
            "Additional Payment": additional_payment,
            "Lump Sum Payment": lump_sum_payment if month == lump_sum_month else 0,
            "Interest Payment": interest_payment,
            "Principal Payment": principal_payment,
            "Percent": interest_percentage,
            "Total Principal Payment": total_principal_payment,
            "Remaining Principal": remaining_principal
        })

        if remaining_principal == 0:
            break

    return amortization_schedule