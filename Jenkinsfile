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
        stage('Deploy to Production') {
            steps {
                // וודא שה-ID כאן תואם למה שהגדרת ב-Jenkins Credentials
                sshagent(['prod-server-ssh']) {
                    script {
                        def PROD_SERVER_IP = "1.2.3.4" // ממליץ להעביר לבלוק environment למעלה
                        
                        echo "Deploying to Production Server: ${PROD_SERVER_IP}"
                        
                        // שימוש בגרשיים כפולים משולשים מאפשר להשתמש במשתני ה-environment של Jenkins
                        sh """
                            ssh -o StrictHostKeyChecking=no ec2-user@${PROD_SERVER_IP} "
                                # 1. התחברות ל-ECR (חייב IAM Role על שרת ה-Prod)
                                aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${REGISTRY_URL}
                                
                                # 2. משיכת האימג החדש
                                docker pull ${REGISTRY_URL}/${REPO_NAME}:latest
                                
                                # 3. עצירה והסרה של הקונטיינר הישן (אם קיים)
                                docker stop ${IMAGE_NAME} || true
                                docker rm ${IMAGE_NAME} || true
                                
                                # 4. הרצת הקונטיינר החדש
                                # שים לב: אנחנו ממפים את פורט 80 של השרת לפורט 5000 של ה-Flask
                                docker run -d --name ${IMAGE_NAME} -p 80:5000 ${REGISTRY_URL}/${REPO_NAME}:latest
                                
                                # 5. ניקיון אימג'ים ישנים
                                docker image prune -f
                            "
                        """
                    }
                }
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
