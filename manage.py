# #!/usr/bin/env python
# """Django's command-line utility for administrative tasks."""
# import os
# import sys


# def main():
#     os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
#     try:
#         from django.core.management import execute_from_command_line
#     except ImportError as exc:
#         raise ImportError(
#             "Couldn't import Django. Are you sure it's installed and "
#             "available on your PYTHONPATH environment variable? Did you "
#             "forget to activate a virtual environment?"
#         ) from exc
#     execute_from_command_line(sys.argv)


# if __name__ == '__main__':
#     main()
#!/usr/bin/env python
import os
import sys
import threading

def run_flask_app():
    # Add the directory containing detection.py to the Python path
    detection_dir = 'exam\detection.py'  # Replace this with the actual path
    sys.path.append(detection_dir)

    # Import and run the Flask app for proctoring
    from detection import app as flask_app
    flask_app.run(debug=True)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'onlinexam.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    # Start Flask app in a separate thread
    flask_thread = threading.Thread(target=run_flask_app)
    flask_thread.start()

    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()

