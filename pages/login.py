from utils.auth import check_login, register_user
from static.elements import gradient_button, gradient_text

import streamlit as st

countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola", "Antigua and Barbuda", "Argentina", "Armenia",
    "Australia", "Austria", "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium",
    "Belize", "Benin", "Bhutan", "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei", "Bulgaria",
    "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia", "Cameroon", "Canada", "Central African Republic", "Chad",
    "Chile", "China", "Colombia", "Comoros", "Congo, Democratic Republic of the", "Congo, Republic of the",
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica", "Dominican Republic",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea", "Estonia", "Eswatini", "Ethiopia", "Fiji",
    "Finland", "France", "Gabon", "Gambia", "Georgia", "Germany", "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary", "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati", "Korea, North",
    "Korea, South", "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia", "Lebanon", "Lesotho", "Liberia", "Libya",
    "Liechtenstein", "Lithuania", "Luxembourg", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali", "Malta",
    "Marshall Islands", "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova", "Monaco", "Mongolia",
    "Montenegro", "Morocco", "Mozambique", "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands", "New Zealand",
    "Nicaragua", "Niger", "Nigeria", "North Macedonia", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
    "Paraguay", "Peru", "Philippines", "Poland", "Portugal", "Qatar", "Romania", "Russia", "Rwanda", "Saint Kitts and Nevis",
    "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
    "Senegal", "Serbia", "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia", "Solomon Islands", "Somalia",
    "South Africa", "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden", "Switzerland", "Syria", "Taiwan", "Tajikistan",
    "Tanzania", "Thailand", "Timor-Leste", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
    "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen", "Zambia", "Zimbabwe"
]

def open_register_dialog():
    with st.form("register_form", border=False):
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First name")
        last_name = col2.text_input("Last name")
        email = col1.text_input("Email")
        country = col2.selectbox("Country", countries)
        password = col1.text_input("Password", type="password")
        repeat_password = col2.text_input("Repeat password", type="password")
        password_hint = st.text_input("Password hint")
        marketing_preferences = st.checkbox("Opt out of communications")
        terms_and_conditions = st.checkbox("I agree to the Terms of Use")

        if st.form_submit_button("Register", use_container_width=True, type='primary'):
            if password != repeat_password:
                st.error("Passwords do not match.")
            elif not first_name or not last_name or not email or not password:
                st.error("All fields are required.")
            else:
                register_user(first_name, last_name, email, country, password, password_hint)

def LoginPage():
    with st.container(border=False):
        col1, col2, col3 = st.columns([1,3,1], vertical_alignment="top")
        
        with col2:
            st.image(image="static/analytiq_type_logo.png", use_container_width=True)

            st.markdown("")

            with st.container(border=False):

                st.markdown(
                    """
                    <div style="text-align: center; font-size: 1rem; color: "#3c3c3c";>
                        Log in to your account
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                email_input = st.text_input("Email")
                password_input = st.text_input("Password", type="password")
                col1, col2 = st.columns(2, vertical_alignment="top")
                #col1.checkbox("Remember Me")
                col1.button("**Forgot Password?**", type="tertiary")
                login_button = st.button(key="login_button", label="Log In", use_container_width=True, type='secondary', icon=":material/login:")

            st.markdown(
                """
                <div style="display: flex; align-items: center; text-align: center; margin: 5px 0px 15px 0px;">
                    <hr style="flex-grow: 1; border: none; border-top: 1px solid #E8E8E8;" />
                    <span style="margin: 0 30px; color: #E8E8E8; font-size: 1rem;">or</span>
                    <hr style="flex-grow: 1; border: none; border-top: 1px solid #E8E8E8;" />
                </div>
                """,
                unsafe_allow_html=True
            )

            @st.dialog("Sign Up")
            def sign_up():
                with st.form("sign_up_form", border=False):
                    col1, col2 = st.columns(2)
                    first_name = col1.text_input("First name")
                    last_name = col2.text_input("Last name")
                    email = col1.text_input("Email")
                    country = col2.selectbox("Country", countries)
                    password = col1.text_input("Password", type="password")
                    repeat_password = col2.text_input("Repeat password", type="password")
                    password_hint = st.text_input("Password hint")
                    marketing_preferences = st.checkbox("Opt out of communications")
                    terms_and_conditions = st.checkbox("I agree to the Terms of Use")

                    if st.form_submit_button("Sign Up", use_container_width=True, type='secondary', icon=":material/app_registration:"):
                        if password != repeat_password:
                            st.error("Passwords do not match.")
                        elif not first_name or not last_name or not email or not password:
                            st.error("All fields are required.")
                        else:
                            register_user(first_name, last_name, email, country, password, password_hint)

            if st.button("Sign Up For Free!", icon=":material/app_registration:", use_container_width=True):
                sign_up()
        
            if login_button:
                user_id, email, first_name, last_name, subscription_level = check_login(email_input, password_input)
                if email:
                    # Reset the logged_out state when logging in successfully
                    st.session_state["logged_out"] = False
                    st.session_state["logged_in"] = True
                    st.session_state["user_id"] = user_id
                    st.session_state["first_name"] = first_name
                    st.session_state["last_name"] = last_name
                    st.session_state["email"] = email
                    st.session_state["subscription_level"] = subscription_level

                    st.success(f"Logged in successfully as {first_name}!")
                    st.session_state["current_page"] = "Dashboard"

                    st.rerun()
                else:
                    st.error("Incorrect email or password. Please try again.")  

if __name__ == "__main__":
    LoginPage()
