import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import time
from streamlit_autorefresh import st_autorefresh

# CSS for alert text and section borders
st.markdown("""
    <style>
    .alert-text {
        color: red;
        font-weight: bold;
        font-size: 16px;
        margin-top: -10px;
    }
    .section-container {
        border: 2px solid #ddd;
        padding: 15px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    .section-title {
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for page navigation and data storage
if "page" not in st.session_state:
    st.session_state["page"] = "home"
if "babies" not in st.session_state:
    st.session_state["babies"] = []
if "selected_baby" not in st.session_state:
    st.session_state["selected_baby"] = None

count = st_autorefresh(interval=60000)

# Function to display the homepage with baby profiles
def show_homepage():
    st.title("Baby Data Monitoring")

    max_babies = 10  # Limit for the maximum number of babies
    current_babies = len(st.session_state["babies"])  # Current number of added babies

    # Display the number of babies added out of the maximum limit
    st.subheader(f"{current_babies}/{max_babies} Babies")

    # Display baby profiles in a grid
    for i in range(0, current_babies, 2):
        col1, col2 = st.columns(2)
        for j, col in enumerate([col1, col2]):
            if i + j < current_babies:
                baby = st.session_state["babies"][i + j]

                # Calculate if feeding is due based on the custom feeding interval in hours and minutes
                time_since_feeding = datetime.now() - baby["last_feeding"]
                feeding_interval = timedelta(
                    hours=baby["feeding_interval_hours"], 
                    minutes=baby["feeding_interval_minutes"]
                )
                needs_feeding = time_since_feeding > feeding_interval

                # Display baby profile with an alert message if feeding is due
                with col:
                    if baby["image"]:
                        st.image(baby["image"], width=150, caption=baby["name"])
                    else:
                        st.write(f"Please upload an image for {baby['name']}")

                    if needs_feeding:
                        st.warning("🔔 It's feeding time!")
                        # Button to mark feeding as done, which resets the last feeding time
                        if st.button(f"Feeding Done for {baby['name']}", key=f"feed_done_{baby['name']}"):
                            baby["last_feeding"] = datetime.now()
                            st.session_state["babies"][i + j] = baby  # Update session state
                            st.rerun()  # Refresh the page

                    # Button to go to baby's detail page
                    if st.button(f"View {baby['name']}'s Data", key=f"view_{baby['name']}"):
                        st.session_state["selected_baby"] = baby
                        st.session_state["page"] = "details"
                        st.rerun()  # Refresh the page

    # Button to add a new baby if the limit hasn't been reached
    if current_babies < max_babies:
        if st.button("Add New Baby"):
            st.session_state["page"] = "add_baby"
            st.rerun()  # Refresh the page
    else:
        st.write("Maximum number of babies reached.")

# Function to display the details page with message board content
def show_details_page():
    baby = st.session_state["selected_baby"]
    st.title(f"{baby['name']}'s Data")

    # Basic Info Section with borders
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Basic Information</div>', unsafe_allow_html=True)
    room_no = st.text_input("Room No:", value=baby.get("room_no", ""))
    mummy_name = st.text_input("Mummy:", value=baby.get("mummy_name", ""))
    checkout_date = st.date_input("Checkout Date", value=baby.get("checkout_date", datetime.now()))
    photoshoot_date = st.date_input("Photoshoot Date", value=baby.get("photoshoot_date", datetime.now()))
    cot_sheet_change_date = st.date_input("Cot Sheet Change Date", value=baby.get("cot_sheet_change_date", datetime.now()))
    amt_range = st.text_input("Amt Range:", value=baby.get("amt_range", ""))
    frequency = st.text_input("Frequency:", value=baby.get("frequency", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    # Feeding Schedule Section with borders
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Feeding Schedule</div>', unsafe_allow_html=True)
    feeding_hours = st.number_input(
        "Feeding Interval Hours", min_value=0, max_value=23, value=baby.get("feeding_interval_hours", 3)
    )
    feeding_minutes = st.number_input(
        "Feeding Interval Minutes", min_value=0, max_value=59, value=baby.get("feeding_interval_minutes", 0)
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # Time and Remarks Section with borders
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Time and Remarks</div>', unsafe_allow_html=True)
    if "time_remarks_data" not in baby:
        baby["time_remarks_data"] = pd.DataFrame(columns=["Time", "Remark"])
    st.write("Current Time and Remarks")
    st.dataframe(baby["time_remarks_data"])
    new_time = st.time_input("Enter Time")
    new_remark = st.text_input("Enter Remark")
    if st.button("Add Remark"):
        new_entry = pd.DataFrame({"Time": [new_time], "Remark": [new_remark]})
        baby["time_remarks_data"] = pd.concat(
            [baby["time_remarks_data"], new_entry], ignore_index=True
        )
        st.success("Remark added successfully.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Appointments and Bookings Section with borders
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Appointments and Bookings</div>', unsafe_allow_html=True)
    mother_baby_care_date = st.date_input("Mother and Baby Care Date", value=baby.get("mother_baby_care_date", datetime.now()))
    mother_baby_care_time = st.time_input("Mother and Baby Care Time", value=baby.get("mother_baby_care_time", datetime.now().time()))
    parent_craft = st.text_input("Parent Craft:", value=baby.get("parent_craft", ""))
    return_demo_bath = st.text_input("Return Demo Bath:", value=baby.get("return_demo_bath", ""))
    breast_massage = st.text_input("Breast Massage:", value=baby.get("breast_massage", ""))
    infant_massage = st.text_input("Infant Massage:", value=baby.get("infant_massage", ""))
    pd_gyne_appointment = st.text_input("PD/GYNE Appointment:", value=baby.get("pd_gyne_appointment", ""))
    lactation_consultant = st.text_input("Lactation Consultant:", value=baby.get("lactation_consultant", ""))
    st.markdown('</div>', unsafe_allow_html=True)

    # Save All Information Button
    if st.button("Save All Information"):
        baby.update({
            "room_no": room_no,
            "mummy_name": mummy_name,
            "checkout_date": checkout_date,
            "photoshoot_date": photoshoot_date,
            "cot_sheet_change_date": cot_sheet_change_date,
            "amt_range": amt_range,
            "frequency": frequency,
            "feeding_interval_hours": feeding_hours,
            "feeding_interval_minutes": feeding_minutes,
            "mother_baby_care_date" : mother_baby_care_date,
            "mother_baby_care_time" : mother_baby_care_time,
            "parent_craft" : parent_craft,
            "return_demo_bath" : return_demo_bath,
            "breast_massage" : breast_massage,
            "infant_massage" : infant_massage,
            "pd_gyne_appointment" : pd_gyne_appointment,
            "lactation_consultant" : lactation_consultant
        })
        st.session_state["babies"][st.session_state["babies"].index(baby)] = baby  # Update in session state
        st.success("All information saved successfully.")

    # Back to Home button
    if st.button("Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()  # Refresh the page

# Function to display the "Add New Baby" form
def show_add_baby_page():
    st.title("Add a New Baby")

    with st.form("Add Baby Form"):
        new_baby_name = st.text_input("Baby Name")
        new_baby_image = st.file_uploader("Upload Baby Image", type=["jpg", "png"])

        # Submit button
        if st.form_submit_button("Add Baby"):
            if new_baby_name and new_baby_image:
                # Add the new baby to the session state
                new_baby = {
                    "name": new_baby_name,
                    "image": new_baby_image,
                    "last_feeding": datetime.now(),
                    "feeding_interval_hours": 3,  # Default feeding interval of 3 hours
                    "feeding_interval_minutes": 0,  # Default additional minutes
                    "next_feeding": datetime.now() + timedelta(hours=3),
                    "next_cot_change": datetime.now() + timedelta(hours=8)
                }
                st.session_state["babies"].append(new_baby)
                st.success(f"Baby {new_baby_name} added successfully!")
                st.session_state["page"] = "home"
                st.rerun()  # Refresh the page
            else:
                st.warning("Please fill in all fields.")

    # Back to Home button
    if st.button("Back to Home"):
        st.session_state["page"] = "home"
        st.rerun()  # Refresh the page

# Page routing logic based on the current page in session state
if st.session_state["page"] == "home":
    show_homepage()
elif st.session_state["page"] == "details":
    show_details_page()
elif st.session_state["page"] == "add_baby":
    show_add_baby_page()

#st.rerun()
