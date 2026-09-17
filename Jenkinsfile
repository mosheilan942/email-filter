pipeline {
    agent { docker { image 'python:3.12-slim' } }
    options {
        skipStagesAfterUnstable()
        buildDiscarder logRotator(removeLastBuild: true)
    }
stages {
  stage('lint') {
    steps {
      sh '''
      python -m venv .venv
      ls -shall
      . .venv/bin/activate
      pip install ruff djlint
      ruff check app.py
      '''
    }
  }
  stage('Test') {
    steps {
      echo 'Nice'
    }
  }
  stage('Build') {
    steps {
      echo 'Nice'
    }
  }
  stage('Push') {
    steps {
      echo 'Nice'
    }
  }
post {
        // Clean after build
        always {
            cleanWs(cleanWhenNotBuilt: true,
                    deleteDirs: true,
                    cleanWhenFailure: true)
        }
    }
}
}
