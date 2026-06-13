pipeline {
    triggers {
        githubPush()
    }
    agent any

    environment {
        IMAGE_NAME = "cloud-erp-fastapi"
    }

    stages {

        stage('Check Files') {
            steps {
                sh 'ls -la'
                sh 'ls -la fastapi_service/.env || true'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build --no-cache -t $IMAGE_NAME ./fastapi_service'
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
                --network cloud_erp_integration_erp-network \
                -p 8000:8000 \
                --env-file fastapi_service/.env \
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
