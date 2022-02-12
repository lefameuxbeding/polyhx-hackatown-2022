# Build from project root folder
# From https://rasa.com/docs/rasa/2.x/how-to-deploy#building-an-action-server-image

ARG RASA_SDK_VERSION=2.8.4
FROM rasa/rasa-sdk:${RASA_SDK_VERSION}

# Set /app as working directory
WORKDIR /app

# Copy additional custom requirements
COPY actions-requirements.txt .

# Change back to root user to install dependencies
USER root

# Install extra requirements for actions
RUN pip install -r actions-requirements.txt

# Copy credentials
COPY action-server/credentials.yml .
# Copy actions folder to working directory
COPY ./* ./actions

# By best practices, don't run the code with root user
USER 1001