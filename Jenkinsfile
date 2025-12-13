pipeline {
    agent any

    environment {
        GCP_PROJECT = "annular-beacon-480011-m2"
        GCLOUD_PATH = "/var/jenkins_home/google-cloud-sdk/bin"
    }

    stages {

        stage('Clone GitHub Repo') {
            steps {
                echo 'Cloning GitHub repo...'
                checkout scmGit(
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        credentialsId: 'github-token',
                        url: 'https://github.com/PREMNATH1311/Hotel_reservation_using-GCP-jenkins.git'
                    ]]
                )
            }
        }

        stage('Build & Push Docker Image') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}
                    gcloud auth configure-docker --quiet

                    # Build Docker image (training happens inside)
                    docker build --no-cache -t gcr.io/${GCP_PROJECT}/ml-project:latest .

                    # Push to GCR
                    docker push gcr.io/${GCP_PROJECT}/ml-project:latest
                    '''
                }
            }
        }

        stage('Deploy to Cloud Run') {
            steps {
                withCredentials([file(credentialsId: 'gcp-key', variable: 'GOOGLE_APPLICATION_CREDENTIALS')]) {
                    sh '''
                    export PATH=$PATH:${GCLOUD_PATH}
                    gcloud auth activate-service-account --key-file=${GOOGLE_APPLICATION_CREDENTIALS}
                    gcloud config set project ${GCP_PROJECT}

                    gcloud run deploy ml-project \
                        --image=gcr.io/${GCP_PROJECT}/ml-project:latest \
                        --platform=managed \
                        --region=us-central1 \
                        --allow-unauthenticated \
                        --set-env-vars CLOUD_RUN=true
                    '''
                }
            }
        }
    }
}
