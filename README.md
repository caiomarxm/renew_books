# renew_books
A Python script to automatically renovate book loans on a library system as return dates get closer.

## System Requisites
- Mozilla's Geckodriver installed and added to path
- Selenium library installed

## Instructions
### Login Information
To effectively use renew_books, inside the "dist" file create a JSON file named "login_info.json" with a single division:

{
"login": your_library_number_here, 
"password": password_here
}

### Autorun on Boot (Windows)
Create a shortcut for "renew_books_UFMG.exe", which is inside "dist", and add it to C:\Users\YOUR_USER_HERE\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup

The application will run on every boot and generate a log.txt inside "dist" so you can check if all renovations were successful.
