import streamlit as st
import datetime
import time

babies = [
    {
        "name": "Harvey",
        "room_no": 401,
        "mummy_name": "YL",
        "checkout_date": "2024-08-08",
        "feeding_times": [
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(8, 30)),
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(11, 30)),
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(14, 30))
            ],
        "last_feed_time": None,
        "feeding_amount": 55,
        "feeding_frequency_hour": 3 
    },
    {
        "name": "Lily",
        "room_no": 402,
        "mummy_name": "Anna",
        "checkout_date": "2024-08-09",
        "feeding_times": [
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(9, 0)),
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(12, 0)),
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(15, 0))
            ],
        "last_feed_time": None,
        "feeding_amount": 30,
        "feeding_frequency_hour": 1 
    },
    {
        "name": "James",
        "room_no": 403,
        "mummy_name": "Sophia",
        "checkout_date": "2024-08-10",
        "feeding_times": [
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(7, 30)),
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(10, 30)),
                datetime.datetime.combine(datetime.datetime.today(), datetime.time(13, 30))
            ],
        "last_feed_time": None,
        "feeding_amount": 100,
        "feeding_frequency_hour": 2 
    }
]

# Initialize babies only once with fixed feeding times
if "babies" not in st.session_state:
    st.session_state.babies = babies

# Function to get the latest feeding time
def get_last_feeding_time(baby):
    return max(baby["feeding_times"])

# Function to calculate the next feeding time
def get_next_feeding_time(baby):
    last_feeding_time = get_last_feeding_time(baby)
    success = update_baby_by_name("Harvey", {"last_feed_time": last_feeding_time})
    if success:
        st.success("baby's details updated!")
    else:
        st.error("Baby not found!")
    return last_feeding_time + datetime.timedelta(hours=baby["feeding_frequency_hour"])

# Function to check if the next feeding time is within the next 5 minutes
def is_feeding_time(baby):
    next_feeding_time = get_next_feeding_time(baby)
    return abs((next_feeding_time - datetime.datetime.now()).total_seconds()) <= 300

# Function to update baby details by name
def update_baby_by_name(name, new_values):
    for baby in st.session_state.babies:
        if baby["name"] == name:
            for key, value in new_values.items():
                if key in baby:
                    baby[key] = value
            return True
    return False  # Baby not found

# Streamlit app
st.title("Baby Dashboard")

def get_current_time():
    return datetime.datetime.now()

# Display all baby boxes with notification
clicked_baby = None  # Stores the currently clicked baby for modal
current_time = get_current_time()  # Check the current time every 10 seconds

for i, baby in enumerate(st.session_state.babies):
    col1, col2 = st.columns([1, 4])
    with col1:
        if is_feeding_time(baby):
            st.markdown(
                f"<div style='animation: blink 1s linear infinite; color: red;'>🔔</div>",
                unsafe_allow_html=True
            )  # Blinking icon if feeding time is reached
    with col2:
        if st.button(f"{baby['name']}"):
            clicked_baby = baby  # Set the clicked baby to display details

# Modal with baby details
if clicked_baby:
    st.markdown(f"### {clicked_baby['name']} Details")
    st.write(f"Room No: {clicked_baby['room_no']}")
    st.write(f"Mummy Name: {clicked_baby['mummy_name']}")
    st.write(f"Checkout Date: {clicked_baby['checkout_date']}")
    st.write(f"Last Feeding Time: {clicked_baby['last_feed_time'].strftime('%Y-%m-%d %H:%M:%S')}")
    st.write(f"Current Time: {get_current_time().strftime('%Y-%m-%d %H:%M:%S')}")

    if is_feeding_time(clicked_baby):
        st.warning("🔔 It's feeding time!")
    else:
        st.success("All is well.")

# CSS for blinking notification icon
st.markdown("""
<style>
@keyframes blink {
    0% { opacity: 1; }
    50% { opacity: 0; }
    100% { opacity: 1; }
}
</style>
""", unsafe_allow_html=True)

time.sleep(10)
st.rerun()