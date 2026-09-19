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
stage('Smoke test') {
    agent any
    steps {
        script {
            sh '''
                docker run -d --name smoke-test -p 5001:5001 \
                  local-registry:5000/my-flask-app:${BUILD_NUMBER}
                sleep 3
            '''
            sh '''
            sh 'curl -v http://docker:5001/ 2>&1 || true'
            '''
            def status = sh(
                script: 'curl -s -o /dev/null -w "%{http_code}" http://docker:5001/',
                returnStdout: true
            ).trim()
            sh 'docker logs smoke-test'
            sh 'docker rm -f smoke-test'
            if (status != '200') {
                error "Smoke test failed: expected 200, got ${status}"
            }
        }
    }
}
}
post {
        // Clean after build
        always {
            sh 'docker rm -f smoke-test'
            junit testResults: 'reports/pytest-report.xml', allowEmptyResults: true
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.git', type: 'INCLUDE'],
                              [pattern: 'reports/*', type: 'EXCLUDE']])
        }
    }
}
