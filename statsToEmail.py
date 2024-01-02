import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import psutil
import platform
import cpuinfo
import GPUtil
import subprocess
import distro

def get_linux_distro_and_de():
    try:
        distro_info = f"{distro.name()} {distro.version()}"
    except distro.DistroWatchError:
        distro_info = 'Not available'

    # Get Desktop Environment (DE) name
    try:
        de_name = subprocess.check_output(["echo $XDG_CURRENT_DESKTOP"], shell=True, universal_newlines=True).strip()
    except subprocess.CalledProcessError:
        de_name = 'Not available'

    return distro_info, de_name

def get_system_info():
    # Processor information
    processor_info = platform.processor()

    # RAM information
    ram_info = psutil.virtual_memory()
    total_ram = ram_info.total
    used_ram = ram_info.used
    ram_percentage = (used_ram / total_ram) * 100

    # Operating System information
    os_name = platform.system()

    # CPU information
    cpu_info = cpuinfo.get_cpu_info()
    cpu_name = cpu_info['brand_raw']

    # CPU usage
    cpu_usage = psutil.cpu_percent()

    # Hostname
    hostname = platform.node()

    # GPU information
    try:
        gpus = GPUtil.getGPUs()
        gpu_info = f"GPU: {gpus[0].name} | Memory: {gpus[0].memoryFree} MB free / {gpus[0].memoryTotal} MB total"
    except Exception as e:
        gpu_info = "GPU information not available"

    # Linux distribution and Desktop Environment
    distro_name, de_name = get_linux_distro_and_de()

    # Create a string with each information section on a new line
    system_info_string = (
        f'<div style="display: inline-block; float: left;"><img width="300" height="406" src="https://i.pinimg.com/736x/20/c7/8a/20c78afdb4ba5424bedc01df48fbce6e.jpg"></div>'
        f'<div style="margin-left: 5px;"><h2>System information report, Sir</h2><br>'
        f"<b>Hostname:</b>{hostname}<br>"
        f"<b>RAM:</b> {used_ram / (1024 ** 3):.2f} GB of {total_ram / (1024 ** 3):.2f} GB ({ram_percentage:.2f}% used)<br>"
        f"<b>Operating System:</b> {os_name}<br>"
        f"<b>Linux Distribution:</b> {distro_name}<br>"
        f"<b>Desktop Environment:</b> {de_name}<br>"
        f"<b>CPU:</b> {cpu_name}<br>"
        f"<b>CPU Usage:</b> {cpu_usage}%<br>"
        f"<b>GPU:</b> {gpu_info}<br></div></div>"
    )

    return system_info_string




def send_email(subject, body, to_email):
    # Gmail SMTP settings or some another smtp server
    smtp_server = "smtp.gmail.com" 
    port = 465
    sender_email = ""  # Your Gmail address
    password = ""  # Your Gmail password

    # Create a MIME message
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "html"))

    # Establish a secure connection to the SMTP server
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        # Log in to your Gmail account
        server.login(sender_email, password)

        # Send the email
        server.sendmail(sender_email, to_email, message.as_string())

sender_email = ""  # Enter your address
receiver_email = ""  # Enter receiver address
password = ""
message = get_system_info();

send_email("System hardware statistic my lord", get_system_info(), receiver_email)