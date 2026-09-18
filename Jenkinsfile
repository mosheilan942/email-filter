#!/usr/bin/env groovy

pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
        buildDiscarder logRotator(removeLastBuild: true)
    }
stages {
  stage('Checkout') {
    agent any
    steps {
    //   stash name: 'source', includes: '**'
      sh 'ls -shall'
    }
  }
  stage('lint') {
  agent { docker { image 'python:3.12-slim' 
                  args '-u 1000:1000' 
                 } 
        }
    steps {
      sh '''
      python -m venv .venv
      . .venv/bin/activate
      pip install ruff djlint
      ruff check app.py
      '''
    }
  }
  stage('Test') {
  agent { docker { image 'python:3.12-slim' 
                  args '-u 1000:1000' } }
    steps {
      sh '''
      . .venv/bin/activate
      pip install flask pytest
      pytest -v --junitxml=reports/pytest-report.xml
      '''
    }
  }
  stage('Build') {
    agent any
    steps {
      sh '''
      docker build -t my-flask-app:${BUILD_NUMBER} .
      '''
    }
  }
  stage('Push') {
    agent any
    steps {
      sh '''
      docker tag my-flask-app:${BUILD_NUMBER} local-registry:5000/my-flask-app:${BUILD_NUMBER}
      docker push local-registry:5000/my-flask-app:${BUILD_NUMBER}
      '''
    }
  }
}
post {
        // Clean after build
        always {
            junit testResults: 'reports/pytest-report.xml', allowEmptyResults: true
            cleanWs(cleanWhenNotBuilt: true,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.gitignore', type: 'EXCLUDE'],
                              [pattern: 'reports/*', type: 'EXCLUDE']])
        }
    }
}
