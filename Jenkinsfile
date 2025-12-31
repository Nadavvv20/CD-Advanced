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
                // כאן נכנס התיקון - הכל עטוף ב-script
                script { 
                    echo 'Starting Smoke Test...'
                    
                    // הרצת הקונטיינר בנפרד
                    sh "docker run -d --name flask-test-container -p 5000:5000 ${IMAGE_NAME}:${BUILD_NUMBER}"
                    
                    try {
                        echo 'Waiting for Flask to boot...'
                        sleep 5 
                        
                        echo 'Checking if the app is responsive...'
                        // שימוש ב-curl לבדיקת השרת
                        sh 'curl -f http://localhost:5000 || exit 1'
                        
                        echo 'Test Passed Successfully!'
                        
                    } catch (Exception e) {
                        echo "Test Failed: ${e.message}"
                        error "Application did not respond with 200 OK"
                    } finally {
                        echo 'Cleaning up test container...'
                        sh 'docker stop flask-test-container || true'
                        sh 'docker rm flask-test-container || true'
                    }
                }
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
