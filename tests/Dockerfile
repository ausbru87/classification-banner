# Use a base image with Ubuntu or a similar distribution
FROM ubuntu:22.04

# Install Gnome3, X11, Xvfb, and other dependencies
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
    gnome-session \
    xorg \
    xvfb \
    python3-gi \
    python3-xlib \
    python3-pip \
    dbus-x11 \
    --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install any Python dependencies your application requires
# COPY requirements.txt /app/requirements.txt
# RUN pip3 install -r /app/requirements.txt

# # Copy your application code to the container
# COPY . /app

# # Set the working directory
# WORKDIR /app

# Start Xvfb in the background
CMD ["sh", "-c", "Xvfb :99 -screen 0 1024x768x16 & pytest tests"]

# Set DISPLAY to use Xvfb
ENV DISPLAY=:99
