## Title
App Music with Django
## Description
Application that let's you upload, store, and play all of your music from the cloud. You can now manage and listen to your music from any device, anywhere in the world.
## Running
1. Create a virtual environment to isolate the application dependencies:

   ```
   python -m venv venv
   ```

2. Activate the virtual environment:

   - For Windows:

     ```
     venv\Scripts\activate
     ```

   - For macOS and Linux:

     ```
     source venv/bin/activate
     ```

3. Install the required dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:

   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py runserver
   ```

5. nagivate to:

   ```
   http://localhost:8000/music
   ```