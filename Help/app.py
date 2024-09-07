import streamlit as st
import db  # Import your database functions

# Initialize the database
db.create_table()

# Admin Password for Deletion Control
ADMIN_PASSWORD = "12349999"  # Change this to a secure password

# Add custom CSS for styling
st.markdown("""
    <style>
    body {
        background-image: url('shriram.jpg'); /* Update with your image file or URL */
        background-size: cover;
        background-position: center center;
        background-attachment: fixed;
    }
    .title {
        color: #4CAF50;
        font-size: 36px;
        font-family: 'Arial', sans-serif;
        text-align: center;
    }
    .problem-card {
        border: 1px solid #ddd;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .pray-button, .delete-button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 10px;
        cursor: pointer;
        font-size: 14px;
    }
    .pray-button:hover {
        background-color: #45a049;
    }
    .delete-button {
        background-color: #f44336;
    }
    .delete-button:hover {
        background-color: #d32f2f;
    }
    </style>
""", unsafe_allow_html=True)

# Function to reload the problems list
def load_problems():
    if 'problems' not in st.session_state:
        st.session_state.problems = db.get_problems()
    return st.session_state.problems

# Problem submission form
st.markdown('<p class="title">Submit Your Problem for Raam Nam Jap</p>', unsafe_allow_html=True)
with st.form(key='problem_form'):
    problem_title = st.text_input('Title of the Problem')
    problem_description = st.text_area('Description of the Problem')
    submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if problem_title and problem_description:
            db.add_problem(problem_title, problem_description)
            st.success('Your problem has been submitted!')
            st.session_state.problems = db.get_problems()  # Reload problems list
        else:
            st.error('Please fill out both fields.')

st.write('---')
st.markdown('<p class="title">Problems List</p>', unsafe_allow_html=True)

# Display the problems from the database
problems = load_problems()

for problem in problems:
    problem_id, title, description, prayers = problem
    st.markdown(f'''
        <div class="problem-card">
            <h3>{title}</h3>
            <p>{description}</p>
            <p>Prayers: {prayers} Mala</p>
            <button class="pray-button" onclick="window.location.href='/pray?problem_id={problem_id}'">Pray for "{title}". Donate 1 Raam Naam Mala (108)</button>
        </div>
    ''', unsafe_allow_html=True)

    # Button to pray for a problem
    if st.button(f'Pray for "{title}"', key=f'pray_{problem_id}'):
        db.update_prayer_count(problem_id)
        st.success(f'You prayed for "{title}". Thank you for your donation of 1 Raam Naam Mala (108)!')

    # Admin Controls for Deletion
    st.sidebar.header('Admin Controls')
    admin_password = st.sidebar.text_input('Admin Password', type='password')

    if admin_password == ADMIN_PASSWORD:
        if st.button(f'Delete "{title}"', key=f'delete_{problem_id}'):
            db.delete_problem(problem_id)
            st.session_state.problems = db.get_problems()  # Reload problems list
            st.success(f'Problem "{title}" has been deleted.')
    else:
        st.sidebar.warning('Enter the correct password to access admin controls.')
