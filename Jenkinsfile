pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'kavyakota18/appointment-booking:latest'
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'   // Jenkins credential ID for Docker Hub login
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Fetching the latest code from GitHub...'
                git branch: 'main', url: 'https://github.com/Kavyakota8/AppointmentBooking_Devops.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image for Appointment Booking System...'
                script {
                    docker.build(DOCKER_IMAGE)
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                script {
                    docker.withRegistry('https://index.docker.io/v1/', DOCKERHUB_CREDENTIALS) {
                        docker.image(DOCKER_IMAGE).push()
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                echo 'Applying Kubernetes manifests (deployment & service)...'
                sh 'kubectl apply -f deployment.yaml'
                sh 'kubectl apply -f service.yaml'
            }
        }

        stage('Verify Deployment') {
            steps {
                echo 'Verifying that the deployment and service are running...'
                sh 'kubectl get pods'
                sh 'kubectl get svc'
            }
        }
    }

    post {
        success {
            echo '✅ Appointment Booking System Deployed Successfully!'
        }
        failure {
            echo '❌ Pipeline Failed! Please check the Jenkins logs for details.'
        }
    }
}
