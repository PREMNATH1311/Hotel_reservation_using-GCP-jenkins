pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        GCP_PROJECT = "annular-beacon-480011-m2"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub repository'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/PREMNATH1311/Hotel_reservation_using-GCP-jenkins.git'
                    ]]
                )
            }
        }

        stage('Setup Virtual Env & Install Dependencies') {
            steps {
                echo 'Setting up virtual environment'
                sh '''
                python -m venv ${VENV_DIR}
                . ${VENV_DIR}/bin/activate
                pip install --upgrade pip
                pip install -e .
                '''
            }
        }

        stage('Train Model') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo 'Training ML model'
                    sh '''
                    . ${VENV_DIR}/bin/activate
                    export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_APPLICATION_CREDENTIALS}
                    python pipeline/training_pipeline.py
                    '''
                }
            }
        }

        stage('Build & Push Docker Image to GCR') {
            steps {
                withCredentials([file(credentialsId:'gcp-key', variable:'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    echo 'Building and pushing Docker image to GCR'
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet
                    docker build -t gcr.io/${GCP_PROJECT}/ml-project:latest .
                    docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    '''
                }
            }
        }
    }
}
