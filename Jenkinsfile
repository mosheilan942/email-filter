pipeline {
    git branch: 'main', url: 'https://github.com/mosheilan942/email-filter'
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            steps {
               echo 'Build'
            }
        }
        stage('Test') {
            steps {
               echo 'Test'
            }
        }
        stage('E2E') {
        steps {
            echo 'E2E to finish'
        }
      }
        stage('Deploy') {
        steps {
            echo 'Deploy'
        }
      }
  }
}
