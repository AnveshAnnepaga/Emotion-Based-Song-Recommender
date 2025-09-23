# 🎶 Emotion-Based Chatbot Song Recommender

## Project Description

This project is a conversational chatbot that recommends songs to users based on their emotional state. By analyzing natural language input, the chatbot classifies the user's mood into one of seven categories—happy, calm, sad, angry, neutral, fear, or surprise—and retrieves a fitting song from a cloud-based database. The system features a modern command-line interface and includes a secure user authentication system to manage and log personalized interactions.

## Key Features

* **Emotional Analysis:** Utilizes a hybrid approach combining a keyword-based system and sentiment polarity to detect a wide range of emotions.
* **Personalized Recommendations:** Provides real-time song suggestions tailored to the user's current mood.
* **Secure Authentication:** Implements a user sign-up and login system using Clerk's Backend API for secure user management.
* **Persistent Data Storage:** Stores and retrieves songs and logs user interactions in a PostgreSQL database managed by Supabase.
* **Professional Interface:** Features a clean, systematic, and visually appealing command-line interface using the `rich` library.

## Technologies Used

* **Core Language:** Python 3.x
* **Backend:** Supabase (PostgreSQL Database)
* **Authentication:** Clerk Backend API
* **NLP:** `textblob`
* **Terminal UI:** `rich`
* **API Requests:** `requests`
* **Environment Management:** `python-dotenv`

## System Architecture

The system follows a modular architecture with a clear separation of concerns:

-   **CLI (`chatbot.py`)**: The user-facing interface that handles all input/output.
-   **Service Layer (`clerk_service.py`, `emotion_analyzer.py`, `song_recommender.py`)**: Contains the core business logic, including authentication, mood detection, and song fetching.
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