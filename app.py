import streamlit as st
from data_loader import load_customer_data
from preprocessing import preprocess_data
from clustering import perform_clustering
from visualization import plot_clusters
from prediction import prediction
from chatbot import call_gemini_api,mail_call_gemini_api
import pandas as pd
# import google.generativeai as genai
from google import genai
from sklearn.cluster import KMeans
import hydralit_components as hc
import plotly.express as px
import os
from mailfun import send_email
from streamlit_option_menu import option_menu
from sklearn.linear_model import LinearRegression

# --------------- Session State Initialization -----------------
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "name" not in st.session_state:
    st.session_state.name = None
if "df" not in st.session_state:
    st.session_state.df = None


# --------------- Handle Query Parameters -----------------
query_params = st.query_params
if "auth" in query_params and query_params["auth"] == "True":
    st.session_state.authenticated = True
    st.session_state.user_id = query_params.get("user", "")
    st.session_state.name = query_params.get("name", "")


# --------------- Ensure User File Exists -----------------
USER_DATA_FILE = "user.csv"
if not os.path.exists(USER_DATA_FILE):
    pd.DataFrame(columns=["name","Email", "Pass"]).to_csv(USER_DATA_FILE, index=False)

# --------------- AUTHENTICATION SECTION -----------------
if not st.session_state.authenticated:
    st.sidebar.title("segmentrends")
    selected2 = st.sidebar.selectbox("LogIn or SignUp", ["LOG IN", "SIGN UP"])

    # Sign Up Page
    if selected2 == "SIGN UP":
        st.header("Sign Up")
        with st.form(key="signup_form"):
            name1 = st.text_input("Enter your Name")
            email1 = st.text_input("Enter the E-MAIL")
            password1 = st.text_input("Enter the PASSWORD", type="password")
            if st.form_submit_button("SIGN UP"):
                user_file = pd.read_csv(USER_DATA_FILE)
                if email1 in user_file["Email"].values:
                    st.error("Email already exists! Please log in.")
                else:
                    new_user = pd.DataFrame([[name1,email1, password1]], columns=["name","Email", "Pass"])
                    new_user.to_csv(USER_DATA_FILE, mode='a', header=False, index=False)
                    st.success("Successfully signed up! Please log in.")

    # Login Page
    if selected2 == "LOG IN":
        st.header("Login")
        with st.form(key="login_form"):
            name = st.text_input("Enter your Name")
            email = st.text_input("Enter Email")
            password = st.text_input("Enter Password", type="password")
            submitbtn = st.form_submit_button(label="Login")
            if submitbtn:
                user_file = pd.read_csv(USER_DATA_FILE)
                if email in user_file["Email"].values:
                    index = user_file[user_file["Email"] == email].index[0]
                    if password == user_file.loc[index, "Pass"]:
                        st.session_state.name = name
                        st.session_state.authenticated = True
                        st.session_state.user_id = email
                        st.query_params.update(auth=True,user=email,name=name)
                        st.success("Login Successfully!")
                        st.rerun()
                    else:
                        st.error("Invalid email or password!")
                else:
                    st.error("Email does not exist! Please sign up first.")
if st.session_state.authenticated :
    # Sidebar Navigation
    # st.sidebar.title("Navigation")
    # page = st.sidebar.radio("Go to", ["Project Overview", "Segmentation Dashboard","prediction dashboard","Chatbot"],)
    # menu_id = [
    #         {"id": "Project Overview", "label": "Project Overview"},
    #         {"id": "Segmentation Dashboard", "label": "Segmentation Dashboard"},
    #         {"id": "prediction dashboard", "label": "prediction dashboard"},
    #         {"id": "Chatbot", "label": "Chatbot"},
    #         {"id": "↪️ Log Out","label":"↪️ Log Out"},
    #         {"id": "email", "label":"email"},
    #         {"id": "newfun","label":"newfun"}
    #     ]

    # over_theme = {
    #     'txc_inactive': '#FFFFFF',  # white for inactive text
    #     'txc_active': '#FFFFFF',  # white for active text
    #     'bg_color': '#000000',  # black background
    #     'option_active_bg': '#333333',  # dark grey for the active option background (optional)
    #     'option_hover_bg': '#444444'  # slightly lighter grey on hover (optional)
    # }
    # # over_theme = {'txc_inactive':'#808080'}
    # over_theme = {
    #     'txc_inactive': '#FFFFFF',  # Inactive text in gray
    #     'bgcolor': '#FFFFFF'        # A light gray background for the nav bar
    # }
    # over_theme = {
    #     'txc_inactive': '#808080',
    #     'txc_active': '#808080',
    #     'option_active_bg': '#D3D3D3',  # If this key controls the active option background
    #     'bar_bg': '#D3D3D3'             # If this is the key for the nav bar background
    # }

    #
    #     # Create horizontal nav bar
    # page = hc.option_bar(
    #     option_definition=menu_id,
    #     horizontal_orientation=True,
    #     # override_theme=over_theme
    #     )
    # 🎨 Custom CSS Styling
    # st.markdown("""
    #     <style>
    #         html, body, [class*="css"] {
    #             font-family: 'Segoe UI', sans-serif;
    #         }
    #         .gradient-header {
    #             background: linear-gradient(to right, #00c6ff, #0072ff);
    #             color: white;
    #             padding: 20px;
    #             border-radius: 12px;
    #             text-align: center;
    #             box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
    #         }
    #         .card {
    #             background-color: #ffffff10;
    #             padding: 20px;
    #             border-radius: 15px;
    #             box-shadow: 0 4px 20px rgba(0,0,0,0.1);
    #             margin-bottom: 20px;
    #         }
    #         .title {
    #             font-weight: 700;
    #             font-size: 28px;
    #             margin-bottom: 10px;
    #             color: #333;
    #         }
    #         .sub {
    #             font-size: 20px;
    #             color: #555;
    #         }
    #     </style>
    # """, unsafe_allow_html=True)
    over_theme = {
        'txc_inactive': '#FFFFFF',  # white text when inactive
        'txc_active': '#000000',  # black text when active
        'bg_color': '#CCCCCC',  # light gray background
        'option_active_bg': '#FFFFFF'  # white background for active item
    }

    page = option_menu(
        menu_title=None,  # hide the menu title
        options=["Project Overview", "Segmentation Dashboard","prediction dashboard","Chatbot","↪️ Log Out","email"],
        icons=["house", "graph-up", "calculator", "chat-dots"],
        default_index=0,
        orientation="horizontal",
        styles=over_theme
    )
    #
    # page = hc.option_bar(
    #     option_definition=[
    #         {"id": "Project Overview", "label": "Project Overview"},
    #         {"id": "Segmentation Dashboard", "label": "Segmentation Dashboard"},
    #         {"id": "prediction dashboard", "label": "prediction dashboard"},
    #         {"id": "Chatbot", "label": "Chatbot"},
    #         {"id": "↪️ Log Out", "label": "↪️ Log Out"},
    #         {"id": "email", "label": "email"},
    #         {"id": "newfun", "label": "newfun"},
    #     ],
    #     horizontal_orientation=True,
    #     override_theme={"txc_inactive": "#FFFFFF", "menu_background": "#ff4b1f"}
    # )
    with st.sidebar:
        # st.title("Settings 🔧")
        # st.write("Adjust parameters here…")
        st.markdown("### 👤 Logged in as:")
        st.info(st.session_state.name)
        # st.title("user id :" + st.session_state.user_id)
        #
        # if page == "Project Overview":
        #     st.write("— No additional settings —")
        #     st.file_uploader("upload")
        # elif page == "Segmentation Dashboard":
        #     n_clusters = st.slider("Number of Clusters", 2, 10, 3)
        # elif page == "Prediction dashboard":
        #     age = st.number_input("Age", 18, 100, 30)
        #     income = st.number_input("Income", 10000, 200000, 50000)
        # elif page == "Chatbot":  # Chatbot
        #     recipients = st.text_input(
        #         "Notify emails (comma-separated):",
        #         placeholder="alice@example.com, bob@example.com"
        #     )
        # elif page == "email":
        #     st.write("mau")
    if page == "Project Overview":
        st.title("Project Overview")
        st.subheader("Project Title:")
        st.write("**Intelligent Customer Segmentation and Predictive Insights for B2C Growth**")

        st.subheader("Objective:")
        st.write("""
        The objective of this project is to analyze customer behavior, segment them into distinct groups, 
        and predict their future actions to enable personalized marketing strategies and improved customer engagement.
        """)

        st.subheader("Overview:")
        st.write("""
        In modern B2C businesses, customer understanding is critical for growth. 
        This project leverages machine learning to segment customers based on demographics and purchasing behavior.
        A future extension will include predictive analytics to forecast customer purchases, churn, and recommend tailored offers.
        """)

        st.subheader("Problems in Existing Systems:")
        st.markdown("""
        - Lack of proper customer segmentation.
        - Inefficient marketing due to generic campaigns.
        - Difficulty in identifying potential churn.
        - Underutilization of large customer data.
        - Limited predictive capabilities in traditional systems.
        """)

        st.subheader("System Modules Implemented:")
        st.markdown("""
        - Data Collection & Preprocessing (CSV Data)
        - Customer Segmentation using K-Means
        - Visualization Dashboard
        """)

        st.subheader("Future Scope:")
        st.markdown("""
        - Personalized Recommendations using Machine Learning
        - Predictive Analytics (Forecasting Future Purchases)
        - Churn Prediction to Improve Retention
        - Integration with Live E-commerce Data
        """)

        st.subheader("Technologies Used:")
        st.markdown("""
        - Python (Data Processing, Machine Learning)
        - Streamlit (Dashboard)
        - Scikit-Learn (Clustering Algorithms)
        - Matplotlib (Visualization)
        """)

    elif page == "Segmentation Dashboard":
        st.title("Customer Segmentation Dashboard")

        # Load Data
        st.subheader("Step 1: Load Data")
        df = load_customer_data()
        st.write(df.head())

        # Preprocess Data
        df = preprocess_data(df)

        # Clustering
        st.subheader("Step 2: Perform Clustering")
        # n_clusters = st.slider("Select Number of Clusters", 1, 4, 2)
        df, model = perform_clustering(df, n_clusters=4)
        st.write("Clustered Data Sample:")
        st.session_state.df = df
        st.dataframe(st.session_state.df)
        # df.to_csv("Synthetic_Customers_with_Age__Income__SpendingScore__Email.csv")
        # st.session_state.dff = df
        # st.write(df.head())

        # Visualization
        st.subheader("Step 3: Cluster Visualization")
        # plot = plot_clusters(df)
        # st.plotly_chart(plot)
        selected = ['SpendingScore', 'Age']
        corr = df[selected].corr()

        # fig = px.imshow(corr, text_auto=True, color_continuous_scale='Blues', title="📊 Clean Heatmap")
        # fig.update_layout(width=700, height=500, margin=dict(l=50, r=50, t=50, b=50))
        # st.plotly_chart(fig)
        fig2 = px.violin(st.session_state.df, x="Cluster", y="Income", box=True, points="all")
        st.plotly_chart(fig2)
        fig3 = px.scatter_matrix(
            st.session_state.df, dimensions=["Age", "Income", "SpendingScore"],
            color="Cluster", symbol="Gender",
            title="Pairwise Relationships"
        )
        fig3.update_traces(diagonal_visible=False)
        st.plotly_chart(fig3)
        fig4 = px.density_contour(df, x="Income", y="SpendingScore", marginal_x="histogram", marginal_y="histogram")
        st.plotly_chart(fig4)

        fig5 = px.sunburst(st.session_state.df, path=["Cluster", "Gender"], title="Cluster → Gender Breakdown")
        st.plotly_chart(fig5)
        fig6 = px.scatter_3d(
            st.session_state.df, x="Age", y="Income", z="SpendingScore",
            color="Cluster", symbol="Gender",color_continuous_scale="Viridis"
        )
        st.plotly_chart(fig6)
        fig7 = px.parallel_coordinates(
            st.session_state.df, color="Cluster",
            dimensions=["Age", "Income", "SpendingScore"]
        )
        st.plotly_chart(fig7)
        fig8 = px.scatter(
            st.session_state.df, x="Income", y="SpendingScore",
            color="Cluster",  # or "Gender"
            size="Age",
            hover_data=["CustomerID", "Email"],
            color_continuous_scale="Inferno"

        )
        st.plotly_chart(fig8)
        fig9 = px.box(df, x="Gender", y="SpendingScore", points="all")
        st.plotly_chart(fig9)
        fig10 = px.histogram(st.session_state.df, x="Age", nbins=12, color="Cluster", marginal="rug")
        st.plotly_chart(fig10)
        # fig11 = px.sunburst(st.session_state.df, path=["Cluster", "Gender"], title="Cluster → Gender Breakdown")
        # st.plotly_chart(fig11)

        # fig = px.box(df, x='Income', y='SpendingScore', title="📦 spending score distribution")
        # st.plotly_chart(fig)
        st.subheader("📊 Pie Chart - Age distribution")
        pie_fig = px.pie(df, names="Age")
        st.plotly_chart(pie_fig)
        # st.subheader("📊 Pie Chart - gender distribution")
        # pie_fig = px.pie(df, names="Gender")
        # st.plotly_chart(pie_fig)
        masum,pratham,rhushi,ajay = plot_clusters(df)
        st.plotly_chart(masum)
        st.plotly_chart(pratham)
        st.plotly_chart(rhushi)
        st.plotly_chart(ajay)
        # st.pyplot(plot)

        st.write("In future scope, we will implement:")
        st.markdown("""
        - Personalized Product Recommendations
        - Predictive Analytics (Purchase Prediction)
        - Customer Churn Prediction
        - Real-time Data Ingestion from CRM Systems
        """)

    elif page == "prediction dashboard":
        with st.form("form123"):
            df = load_customer_data()
            df = preprocess_data(df)
            userage = st.number_input("enter user age")
            userincome = st.number_input("enter income")
            userspend = st.number_input("enter the wpending score")
            user_data = pd.DataFrame({"Age": [userage], "Income": [userincome],"SpendingScore" : [userspend]})
            pred = prediction(df, user_data,3)
            button = st.form_submit_button("submit")
            st.image("Screenshot 2025-04-18 091113.png")
                       # **Cluster 3**: Low Income, High Spending
                       # **Cluster 4**: Moderate Income, Moderate Spending
                       #
        if button:
           # m =  [ "Premium Customers",  # Income highest, Spending highest
           #   "Savvy Investors",  # Income high, Spending low
           #    "Value Seekers",  # Income low,  Spending high
           #   "Budget Conscious"]
           #  for i in range(4):
           #      if i == pred:
           #          segg = m[i]

            st.write(pred)

        st.header("PREDICTION DASHBOARD")
        reg = LinearRegression()
        reg.fit(df[["Age", "Income"]], df["SpendingScore"])
        with st.form(key="form1"):
            age = st.text_input("Enter a Age")
            income = st.text_input("Enter a Income")
            submit = st.form_submit_button("CLICK")
            if submit:
                Age = float(age)
                Income = float(income)
                pre = reg.predict([[Age, Income]])
                st.success(f" predicted score:{pre[0]}")

                fig = px.scatter(df, x='Age', y='SpendingScore')
                st.header("predict score base on income and age")

                fig.add_scatter(
                    x=df['Age'],
                    y=df['SpendingScore'],
                    mode='markers+text',
                    marker=dict(color='blue', size=8),

                    name='Actual'
                )

                fig.add_scatter(x=[Age], y=[pre][0], marker=dict(color='red', size=10), name='Predicted',
                                mode='markers+text', )
                st.plotly_chart(fig, use_container_width=True)
        st.markdown("### 📊 BAR CHART OF GENDER AND SPENDING SCORES")
        count = df.groupby("Gender")["SpendingScore"].mean()
        st.write(count)

        fig = px.bar(count, x=["Male", "Female"], y="SpendingScore",
                     color_discrete_map={"Male": "pink", "Female": "blue"}, color=["Male", "Female"])
        fig.update_layout(xaxis_title="Gender", yaxis_title="SpendingScore", width=1000, height=500,
                          title="Gender vs Spending Score")
        fig.update_traces(width=0.3)
        st.plotly_chart(fig)

        st.markdown("### 🌐 BAR CHART OF AGE RNAGE AND SPENDING SCORES")
        bins = [0, 20, 30, 40, 50, 60, 70]
        group = ["0-20", "20-30", "30-40", "40-50", "50-60", "60-70"]
        df["Agegroup"] = pd.cut(df["Age"], bins=bins, labels=group, ordered=False)
        groupage = df.groupby("Agegroup")["SpendingScore"].mean()

        fig = px.bar(groupage, x=group, y="SpendingScore",
                     color=group, barmode='group',
                     color_discrete_map={"0-20": "red", "20-30": "yellow", "30-40": "red",
                                         "40-50": "pink", "50-60": "green", "60-70": "gray"})
        fig.update_layout(xaxis_title="Age Groups", yaxis_title="Spending Score (1-100)",
                          title="Age Group vs Spending Score", bargap=0.5)
        fig.update_traces(width=0.5)
        st.plotly_chart(fig)

    elif page == "Chatbot":


        file = st.file_uploader("upload")

        data = pd.read_csv(file)

        if data is not None:

            rows_as_text = data.apply(lambda row: f"Income: {row['Income']}, Age: {row['Age']}SpendingScore :{row['SpendingScore']}", axis=1,)

            # Combine or chunk them
            text_block = "\n".join(rows_as_text.tolist())



            if "messages" not in st.session_state:
                st.session_state.messages = []

            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            if prompt := st.chat_input("what is up ?"):
                with st.chat_message("user"):
                    st.markdown(prompt)
                st.session_state.messages.append({"role": "user", "content": f" {text_block} im providing this dataset to you, answer questions according to this dataset{prompt}"})
                respose = f"{prompt}"
                # with st.chat_message("assistant"):
                #     st.markdown(respose)
                #     st.session_state.messages.append({"role": "user", "content": prompt})
#
            # Hypothetical usage
            # genai.configure(api_key=st.secrets["API_KEY"])
            client = genai.Client(api_key=st.secrets["API_KEY"])

            model_name = "gemini-2.0-flash"  # or whatever your doc says
            messages = [
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ]

            # The library might want a single combined string,
            # or might accept messages like OpenAI.
            # This depends on your doc. Let's assume single string:
            prompt_text = ""
            for msg in messages:
                if msg["role"] == "user":
                    prompt_text += f"User: {msg['content']}\n"
                else:
                    prompt_text += f"Assistant: {msg['content']}\n"
            prompt_text += "Assistant:"

            # Non-streaming call:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt_text
            )

            full_response = response.text  # or list of messages
            st.write(full_response)

            st.session_state.messages.append({"role": "assistant", "content": full_response})
        else:
            st.error("please upload dataset")
    elif page == "email":

        # If you want them as a plain Python list:
        # emails_list = emails_age_19.tolist()
        # st.write(emails_list)
        select = st.selectbox("select ",
                              ["Luxury Watch", "High-End Laptop", "Designer Handbag", "Noise-Cancelling Headphones",
                               "Premium Vacuum", "Classic Jeans", "DSLR Camera", "Quality Mixer", "Standard Smartphone",
                               "Sturdy Backpack", "Wireless Speaker", "Fitness Tracker", "Smart Assistant",
                               "Portable Charger", "Sunglasses", "Basic T-Shirt", "LED Bulb Pack", "Simple Earbuds",
                               "Tote Bag", "Steel Flask"])
        mailresponse = mail_call_gemini_api(select)
        # segmentsel = st.selectbox("select segment you want to target ",["Premium","Savvy","Value Seekers","Budget Conscious"])
        # df = load_customer_data()

        premium_products = [
            "Luxury Watch",
            "High-End Laptop",
            "Designer Handbag",
            "Noise-Cancelling Headphones",
            "Premium Vacuum"
        ]

        savvy_investors_products = [
            "Classic Jeans",
            "DSLR Camera",
            "Quality Mixer",
            "Standard Smartphone",
            "Sturdy Backpack"
        ]

        value_seekers_products = [
            "Wireless Speaker",
            "Fitness Tracker",
            "Smart Assistant",
            "Portable Charger",
            "Sunglasses"
        ]

        budget_conscious_products = [
            "Basic T-Shirt",
            "LED Bulb Pack",
            "Simple Earbuds",
            "Tote Bag",
            "Steel Flask"
        ]
        if select in savvy_investors_products :
            emails_age_19 = st.session_state.df.loc[st.session_state.df['Cluster'] == 2, 'Email']
        elif select in premium_products :
            emails_age_19 = st.session_state.df.loc[st.session_state.df['Cluster'] == 0, 'Email']
        elif select in value_seekers_products:
            emails_age_19 = st.session_state.df.loc[st.session_state.df['Cluster'] == 1, 'Email']
        elif select in budget_conscious_products:
            emails_age_19 = st.session_state.df.loc[st.session_state.df['Cluster'] == 3, 'Email']
            st.write("done")
        st.image("Screenshot 2025-04-18 091113.png")
        st.write("this is the autogenerated mail ,if you want to send this to targeted customer click here ")
        st.info(mailresponse)
        # Streamlit app


        # Instructions
        # st.write("Enter your sender email credentials and a comma-separated list of recipient emails.")

        # Input fields
        sender = "segmentrends@gmail.com"
        sender_password = "qnca umak ngjz gave"  # st.text_input("Sender Password", type="password")
        subject = "hey here we are giving you this coupen code to you" #st.text_input("Email Subject")
        body = mailresponse  #st.text_area("Email Body")
        # recipients_str = st.text_area("Recipient Emails (comma separated)")

        if st.button("Send Email"):

            # Split recipient emails by comma and strip spaces
            # recipients = df.loc[df['Cluster'] == 1, 'Email']
            # st.write(recipients)
            recipients = emails_age_19.tolist()#[email.strip() for email in recipients_str.split(",") if email.strip()]
            st.write(recipients)
            if not recipients:
                st.error("Please enter at least one recipient email.")
            # elif not sender or not sender_password:
            #     st.error("Please enter your sender email and password.")
            else:
                try:
                    send_email(recipients, subject, body)
                    st.success("Email sent successfully!")
                except Exception as e:
                    st.error(f"Error sending email: {e}")
    elif page == "↪️ Log Out":
        st.session_state.authenticated = False
        st.session_state.user_id = None
        st.query_params.clear()
        st.success("Logged out Successfully.......Log In again to use out website")
        st.rerun()
    elif page == "newfun":
        select = st.selectbox("select ",
                              ["Luxury Watch", "High-End Laptop", "Designer Handbag", "Noise-Cancelling Headphones",
                               "Premium Vacuum", "Classic Jeans", "DSLR Camera", "Quality Mixer", "Standard Smartphone",
                               "Sturdy Backpack", "Wireless Speaker", "Fitness Tracker", "Smart Assistant",
                               "Portable Charger", "Sunglasses", "Basic T-Shirt", "LED Bulb Pack", "Simple Earbuds",
                               "Tote Bag", "Steel Flask"])
        mailresponse = mail_call_gemini_api(select)
        st.write(mailresponse)
        # --- Sidebar ----------------------------------------------------


        #
        # st.title("Gemini Chatbot")
        # file = st.file_uploader("hey upload your file ")
        # data = pd.read_csv(file)
        # st.dataframe(data)
        # # Summarize each row as a line of text
        #
        # rows_as_text = data.apply(lambda row: f"Income: {row['Income']}, Age: {row['Age']}SpendingScore :{row['SpendingScore']}", axis=1,)
        #
        # # Combine or chunk them
        # text_block = "\n".join(rows_as_text.tolist())
        # st.write(text_block)
        #
        # user_query = st.text_input("Ask a question:")
        # if st.button("Send"):
        #     #
        #     okgemini = call_gemini_api(text_block,user_query)
        #     st.write(okgemini)
            # main()


            # if user_query.strip():
            #     try:
            #         gemini_response = call_gemini_api(prompt=user_query)
            #         st.write("**Gemini:**", gemini_response)
            #     except Exception as e:
            #         st.error(f"Error calling Gemini: {e}")
            # else:
            #     st.write("Please enter a question.")

