#!/usr/bin/env groovy
@Library('shared-library@v1.0.0') _

properties([
    parameters([
        booleanParam(name: 'TOGGLE', defaultValue: true, description: 'Toggle this value'),
        choice(name: 'CHOICE', choices: ['One', 'Two', 'Three'], description: 'Pick something'),
        password(name: 'PASSWORD', defaultValue: 'SECRET', description: 'Enter a password')
    ])
])
node {
    checkout scm
    // 1. Job-level properties (Run at the very beginning)
    properties([
        disableConcurrentBuilds(),
        buildDiscarder(logRotator(removeLastBuild: true, numToKeepStr: '5'))
    ])

    // environment {
    // DOCKER_REGISTRY = credentials('36304674-ec83-40bf-a83e-7fa73b31f653')
    // 2. Global timeout wrapper
    timeout(time: 5, unit: 'MINUTES') {
        
        
  stage('Use shared library') {
    // Commands run directly inside the stage
    helloWorld(name: "Moshe", userName: "user mosheilan")
}

stage('Checkout & Cleanup') {
    // Replaces: when { branch pattern: "notMain", comparator: "EQUALS"}
    if (env.BRANCH_NAME == 'notMain') {
        // stash name: 'source', includes: '**'
        sh 'ls -shall'
        sh 'docker rm -f smoke-test || true'
    } else {
        echo "Skipping stage because branch is ${env.BRANCH_NAME}, not 'notMain'"
    }
}
  stage('Example') {
        // Now you can safely consume them as shown before:
        echo "Toggle: ${params.TOGGLE}"
        echo "Choice: ${params.CHOICE}"
        echo "Password: ${params.PASSWORD}"
    }
//   stage('Run Tests') {
//     // Parallel steps in Scripted require a map of named closures
//     parallel(
//         'lint': {
//             stage('lint') {
//                 // Replaces: agent { docker { image 'python:3.12-slim' } }
//                 docker.image('python:3.12-slim').inside {
//                     // steps block is removed, commands run directly
//                     sh '''
//                     python -m venv .venv
//                     . .venv/bin/activate
//                     pip install ruff djlint
//                     ruff check app.py
//                     '''
//                 }
//             }
//         },
//         'Test': {
//             stage('Test') {
//                 docker.image('python:3.12-slim').inside {
//                     sh '''
//                     . .venv/bin/activate
//                     pip install flask pytest
//                     pytest -v --junitxml=reports/pytest-report.xml
//                     '''
//                     stash includes: 'reports/*.xml', name: 'test-results'
//                 }
//             }
//         }
//     )
// }

//   stage('Build') {
//       sh '''
//       docker build -t my-flask-app:${BUILD_NUMBER} .
//       '''
//   }
//   stage('Push') {
//       sh '''
//       docker tag my-flask-app:${BUILD_NUMBER} local-registry:5000/my-flask-app:${BUILD_NUMBER}
//       echo "$DOCKER_REGISTRY_PSW" | docker login local-registry:5000 --username "$DOCKER_REGISTRY_USR" --password-stdin
//       docker push local-registry:5000/my-flask-app:${BUILD_NUMBER}
//       '''
//   }
// stage('Smoke test') {
//         script {
//             sh '''
//                 docker run -d --name smoke-test -p 5001:5001 \
//                   local-registry:5000/my-flask-app:${BUILD_NUMBER}
//                 sleep 3
//             '''
//             def status = sh(
//                 script: 'curl -s -o /dev/null -w "%{http_code}" http://docker:5001/',
//                 returnStdout: true
//             ).trim()
//             sh 'docker logs smoke-test'
//             sh 'docker rm -f smoke-test'
//             if (status != '200') {
//                 error "Smoke test failed: expected 200, got ${status}"
//             }
//         }
// }
// stage('Second Stage') {
//             // 3. Manual implementation of skipStagesAfterUnstable()
//             if (currentBuild.result == 'UNSTABLE') {
//                 echo 'Skipping stage due to UNSTABLE build status.'
//                 Utils.markStageSkippedForConditional('Second Stage') // Optional: visually skips in Blue Ocean
//             } else {
//                 echo 'Running second stage...'
//             }
//         }                 
// post {
//         failure {
//             echo 'Build failed! Archiving diagnostic logs and artifacts...'
//             archiveArtifacts artifacts: 'reports/*.xml',
//                                 allowEmptyArchive: true, 
//                                 fingerprint: true,
//                                 onlyIfSuccessful: false
//         }
//         always {
//             sh 'docker rm -f smoke-test'
//             unstash 'test-results'
//             junit testResults: 'reports/pytest-report.xml', allowEmptyResults: true
//             cleanWs(cleanWhenNotBuilt: false,
//                     deleteDirs: true,
//                     disableDeferredWipeout: true,
//                     notFailBuild: true,
//                     patterns: [[pattern: '.git', type: 'INCLUDE'],
//                               [pattern: 'reports/*', type: 'EXCLUDE']])
//         }
//     }
// }

//     if (currentBuild.currentResult != 'SUCCESS') {
//     stage('Deploy') {
//         echo 'Deploy'
//     }
     }

    // }
}
