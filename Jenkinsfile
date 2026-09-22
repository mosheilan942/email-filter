#!/usr/bin/env groovy
@Library('shared-library') _
pipeline {
    agent any
    parameters {
        booleanParam(name: 'TOGGLE', defaultValue: true, description: 'Toggle this value')

        choice(name: 'CHOICE', choices: ['One', 'Two', 'Three'], description: 'Pick something')

        password(name: 'PASSWORD', defaultValue: 'SECRET', description: 'Enter a password')
    }
    options {
        disableConcurrentBuilds()
        skipStagesAfterUnstable()
        buildDiscarder logRotator(removeLastBuild: true, numToKeepStr: '5')
        timeout(time: 5, unit: 'MINUTES') 
    }
    environment {
    DOCKER_REGISTRY = credentials('36304674-ec83-40bf-a83e-7fa73b31f653')
}
stages {
  stage('Use shared library') {
    steps {
      HelloWorld(name: "Moshe", userName: "mosheilan")
    }
  }
  stage('Checkout & Cleanup') {
    when { branch pattern: "notMain", comparator: "EQUALS"}
    steps {
    //   stash name: 'source', includes: '**'
      sh 'ls -shall'
      sh 'docker rm -f smoke-test || true'
    }
  }
  stage('Example') {
            steps {
                echo "Toggle: ${params.TOGGLE}"

                echo "Choice: ${params.CHOICE}"

                echo 'Password: ${params.PASSWORD}'
            }
        }
  stage('Run Tests') {
  parallel {

  stage('lint') {
        agent { docker { image 'python:3.12-slim'  
  } }
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
  } }
    steps {
      sh '''
      . .venv/bin/activate
      pip install flask pytest
      pytest -v --junitxml=reports/pytest-report.xml
      '''
      stash includes: 'reports/*.xml', name: 'test-results'
    }
  }
  }
  }
  stage('Build') {
    steps {
      sh '''
      docker build -t my-flask-app:${BUILD_NUMBER} .
      '''
    }
  }
  stage('Push') {
    steps {
      sh '''
      docker tag my-flask-app:${BUILD_NUMBER} local-registry:5000/my-flask-app:${BUILD_NUMBER}
      echo "$DOCKER_REGISTRY_PSW" | docker login local-registry:5000 --username "$DOCKER_REGISTRY_USR" --password-stdin
      docker push local-registry:5000/my-flask-app:${BUILD_NUMBER}
      '''
    }
  }
stage('Smoke test') {
    steps {
        script {
            sh '''
                docker run -d --name smoke-test -p 5001:5001 \
                  local-registry:5000/my-flask-app:${BUILD_NUMBER}
                sleep 3
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
        failure {
            echo 'Build failed! Archiving diagnostic logs and artifacts...'
            archiveArtifacts artifacts: 'reports/*.xml',
                                allowEmptyArchive: true, 
                                fingerprint: true,
                                onlyIfSuccessful: false
        }
        always {
            sh 'docker rm -f smoke-test'
            unstash 'test-results'
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
