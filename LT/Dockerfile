# Use Ubuntu as the base image
# FROM ubuntu:latest
FROM arm64v8/ubuntu:rolling

# Install Python 3.10 and pip
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3-pip

# Create a symbolic link for Python and Pip
# Update-alternatives for Python and Pip
# RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1 && \
#     update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

#install screen htop psmisc tmux
RUN apt-get install -y screen
RUN apt-get install -y htop
RUN apt-get install -y psmisc
RUN apt-get install -y tmux

# Optionally install additional utilities like vim, wget, etc.
# RUN apt-get install -y vim wget


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app except for trainer_lt.py, utils.py
COPY . /app
RUN rm /app/trainer_lt.py
RUN rm /app/utils.py

# Install any needed packages specified in requirements.txt
RUN pip3 install torch torchvision matplotlib tqdm LiveTune tensorboard psutil


# Expose the ports your application uses
EXPOSE 80

# Expose 8000 to 8010
EXPOSE 8000-8010

# Expose 6006 to 6010
EXPOSE 6006-6012

# Use a non-root user to run the application (optional but recommended for security) 
# make a root user
USER root

# RUN useradd -ms /bin/bash newuser
# USER newuser

# Set the entry point to a shell. This will start a shell when a container starts.
ENTRYPOINT ["/bin/bash"]
