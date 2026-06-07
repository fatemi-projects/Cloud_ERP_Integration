pipeline {
    agent any

    environment {
        IMAGE_NAME = "cloud-erp-fastapi"
    }

    stages {

        stage('Check Files') {
            steps {
                sh 'ls -la'
                sh 'ls -la .env || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME ./fastapi_service'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop fastapi-app || true'
                sh 'docker rm fastapi-app || true'
            }
        }

        stage('Run New Container') {
            steps {
                sh '''
                docker run -d \
                --name fastapi-app \
                -p 8000:8000 \
                --env-file ./.env \
                $IMAGE_NAME
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment Successful"
        }

        failure {
            echo "Deployment Failed"
        }
    }
}