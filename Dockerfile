# Use the official Python 3.9 image as a base image
FROM python:3.11

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements file into the container at /app/requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Add /root/.local/bin to the PATH inside the container
ENV PATH="${PATH}:/root/.local/bin"
# Set the PYTHONPATH environment variable to the current directory inside the container
ENV PYTHONPATH=.

# Upgrade pip and install the Python dependencies specified in requirements.txt
# Use --no-cache-dir to avoid saving the pip cache and reduce the image size
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the src directory from the host to /app/src/ inside the container
COPY src/ /app/src/

# Command to run when the container starts
# Start the Uvicorn server for the FastAPI app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
