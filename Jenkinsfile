pipeline {
    agent { docker { image 'python:3.12-slim' } }
    options {
        skipStagesAfterUnstable()
    }
stages {
  stage('lint') {
    steps {
      pip install ruff
      ruff check app.py
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

}
}
