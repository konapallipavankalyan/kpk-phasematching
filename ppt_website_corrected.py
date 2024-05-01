import numpy as np
import streamlit as st
from scipy.optimize import minimize

# Sellmeier equations for optical materials
def sellmeier_no(lamda):
    n_o = np.sqrt(2.7405 + (0.0184 / (lamda**2 - 0.0179)) - 0.0155 * lamda**2)
    return n_o

def sellmeier_ne(lamda):
    n_e = np.sqrt(2.3753 + (0.01224 / (lamda**2 - 0.01667)) - 0.01516 * lamda**2)
    return n_e

# Type 1 and Type 2 calculations
def type1(lamda, oa):
    n_op = sellmeier_no(lamda)
    n_ep = sellmeier_ne(lamda)
    
    n_e_theta = sellmeier_no(2 * lamda) * (np.cos(np.deg2rad(oa)))
    
    theta_p = np.rad2deg(np.arcsin(np.sqrt((n_ep**2 / n_e_theta**2) * ((n_op**2 - n_e_theta**2) / (n_op**2 - n_ep**2)))))
    return theta_p

def type2(lamda, oa):
    n_op = sellmeier_no(lamda)
    n_ep = sellmeier_ne(lamda)
    n_os = sellmeier_no(2 * lamda)
    n_es = sellmeier_ne(2 * lamda)

    def objective(theta_p):
        c = np.sqrt((n_op**2 * n_ep**2) / (n_ep**2 * np.cos(theta_p)**2 + n_op**2 * np.sin(theta_p)**2))
        d = np.sqrt((n_os**2 * n_es**2) / (n_es**2 * np.cos(theta_p)**2 + n_os**2 * np.sin(theta_p)**2))
        return np.abs((2 * c) - ((n_os + d) * np.cos(np.deg2rad(oa))))

    # Initial guess for theta_p
    initial_guess = 0.5

    # Minimize the objective function
    result = minimize(objective, initial_guess)

    # The optimized value of theta_p in degrees
    theta_p_minimized = np.rad2deg(result.x[0])

    return theta_p_minimized

# Streamlit app to calculate theta_p for Type 1 and Type 2
def main():
    st.title("Sellmeier Equation Calculator")

    # Input for lambda with high precision and small step size
    lamda = st.number_input(
        "Enter the value of lambda",
        min_value=0.1,
        max_value=10.0,
        step=0.001,  # Finer step size
        value=1.0,
        format="%.3f"  # Display with three decimal places
    )

    oa = st.number_input(
        "Enter the value of oa (angle in degrees)",
        min_value=0.0,
        max_value=90.0,
        step=1.0,
        value=45.0
    )

    if st.button("Calculate"):
        theta_p_type1 = type1(lamda, oa)
        theta_p_type2 = type2(lamda, oa)
        
        st.success(f"Type 1 - The calculated theta is: {theta_p_type1:.2f} degrees")
        st.success(f"Type 2 - The optimized theta is: {theta_p_type2:.2f} degrees")

# Run the Streamlit app
if __name__ == "__main__":
    main()
