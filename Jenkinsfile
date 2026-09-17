#!/usr/bin/env groovy

pipeline {
    agent { docker { image 'python:3.12-slim' } }
    options {
        skipStagesAfterUnstable()
        buildDiscarder logRotator(removeLastBuild: true)
    }
stages {
  stage('Checkout') {
    steps {
      sh 'ls -shall'
    }
  }
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
      docker build -t my-flask-app .
      '''
    }
  }
  stage('Push') {
    steps {
      echo 'Nice'
    }
  }
}
post {
        // Clean after build
        always {
            junit testResults: 'reports/pytest-report.xml', allowEmptyResults: true
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.gitignore', type: 'INCLUDE'],
                               [pattern: 'reports/*', type: 'INCLUDE']])
        }
    }
}
