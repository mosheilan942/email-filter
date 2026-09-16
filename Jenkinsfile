pipeline {
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
            echo 'E2E'
        }
      }
        stage('Deploy') {
        steps {
            echo 'Deploy'
        }
      }
  }
}
