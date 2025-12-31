pipeline {
    agent any
    environment {
        IMAGE_NAME = 'nadav-hello-world'
        REGISTRY_URL = '992382545251.dkr.ecr.us-east-1.amazonaws.com'
        REPO_NAME = 'nadav-test-repo'
    }
    stages {
        stage('Build') {
            steps {
                echo 'Building the image...'
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .'
                sh 'docker tag ${IMAGE_NAME}:latest ${REGISTRY_URL}/${REPO_NAME}:latest'
                sh 'docker tag ${IMAGE_NAME}:latest ${REGISTRY_URL}/${REPO_NAME}:${BUILD_NUMBER}'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing the app...'
                sh 'docker run --rm ${IMAGE_NAME}:${BUILD_NUMBER} '
            }
        }
        stage('Push') {
            steps {
                echo 'Authenticating with ECR...'
                sh 'aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${REGISTRY_URL}'
                echo 'Pushing the image to the ECR...'
                sh "docker push ${REGISTRY_URL}/${REPO_NAME}:latest"
                sh "docker push ${REGISTRY_URL}/${REPO_NAME}:${BUILD_NUMBER}"
            }
        }
    }
    post {
        always {
            echo 'Cleaning up Docker resources...'
            sh "docker rmi ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest"
            sh "docker rmi ${REGISTRY_URL}/${REPO_NAME}:latest"
            sh "docker rmi ${REGISTRY_URL}/${REPO_NAME}:${BUILD_NUMBER}"
            
        }
    }
}
