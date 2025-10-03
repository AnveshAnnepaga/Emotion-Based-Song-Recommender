# 🎶 Emotion-Based Chatbot Song Recommender

## Project Description

This project is a conversational chatbot that recommends songs to users based on their emotional state. By analyzing natural language input, the chatbot classifies the user's mood into one of seven categories—happy, calm, sad, angry, neutral, fear, or surprise—and retrieves a fitting song from a cloud-based database. The system features a modern command-line interface and includes a secure user authentication system to manage and log personalized interactions.

## Key Features

* **Emotional Analysis:** Utilizes a hybrid approach combining a keyword-based system and sentiment polarity to detect a wide range of emotions.
* **Custom Web Interface:** Features a clean, visually appealing, dark-mode UI built with Streamlit.
* **Secure Authentication:**  Implements a robust, self-managed user sign-up and login system using bcrypt for industry-standard password hashing and secure verification.
* **Persistent Data Storage:** Stores and retrieves songs and logs user interactions in a PostgreSQL database managed by Supabase.
* **Professional Interface:** Features a clean, systematic, and visually appealing command-line interface using the `rich` library.

## Technologies Used

* **Core Language**: Python 3.x

* **Frontend/UI**: Streamlit (Framework for the modern, professional web interface)

* **Authentication**: bcrypt (Industry-standard library for secure password hashing and verification)

* **Database**: Supabase (PostgreSQL Database)

* NLP**: textblob (Library used for emotion analysis)

* **Terminal Output**: rich (Used for professional console output/debugging)

* **API Requests**: requests (Used by services for internal API calls)

* **Configuration**: python-dotenv (Manages secure environment variables)

## System Architecture

The system follows a modular architecture with a clear separation of concerns:

-   **CLI (`app.py`)**: The user-facing interface that handles all input/output.
-   **Service Layer (`auth_service.py`, `emotion_analyzer.py`, `song_recommender.py`)**: Contains the core business logic, including authentication, mood detection, and song fetching.
-   **DAO Layer (`supabase_client.py`, `user_logger.py`)**: Handles all direct database operations to ensure data integrity and security.
-   **Cloud Services**: The backend is powered by **Supabase** (for the database) and **Clerk** (for user authentication).

## Installation & Setup

Follow these steps to set up and run the project locally.

### 1. Prerequisites

* Python 3.8 or higher
* A free [Supabase](https://supabase.com/) account
* A free [Clerk](https://clerk.com/) account

### 2. Clone the Repository

```sh
git clone https://github.com/AnveshAnnepaga/Emotion-Based-Song-Recommender.git
cd https://github.com/AnveshAnnepaga/Emotion-Based-Song-Recommender.git




### 3. Install Dependencies

Install all the required Python libraries using pip.

```sh
pip install -r requirements.txt