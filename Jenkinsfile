pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
    stages {
        stage('Build') {
            steps {
               docker run helloworld
            }
        }
        stage('Test') {
            steps {
               echo 'Test'
            }
        }
        stage('E2E') {
        steps {
            echo currentBuild.currentResult
            echo currentBuild.displayName
        }
      }
        stage('Deploy') {
        steps {
            echo 'Deploy'
        }
      }
  }
}
