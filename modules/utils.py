from datetime import datetime

def log_complaint(user_text, department, config):
    log_path = config['log']['file_path']
    with open(log_path, "a") as file:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f'"{now}","{user_text}","{department}"\n')
