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
      pip install pytest
      pytest -v --junitxml=reports/pytest-report.xml
      '''
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
post {
        // Clean after build
        always {
            cleanWs(cleanWhenNotBuilt: true,
                    deleteDirs: true,
                    cleanWhenFailure: true
            patterns: [[pattern: 'reports/*', type: 'INCLUDE']]
            )
            junit testResults: 'reports/pytest-report.xml', allowEmptyResults: true
        }
    }
}
