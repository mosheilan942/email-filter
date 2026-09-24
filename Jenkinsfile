#!/usr/bin/env groovy
@Library('shared-library@v1.0.0') _

// =============================================================================
// Job configuration: replaces declarative `parameters {}` and most of `options {}`.
// NOTE: properties() is applied at runtime, so changes take effect from the NEXT build
// (identical to declarative). On the very first build, `params.*` may be null.
// =============================================================================
properties([
    parameters([
        booleanParam(name: 'TOGGLE', defaultValue: true, description: 'Toggle this value'),
        choice(name: 'CHOICE', choices: ['One', 'Two', 'Three'], description: 'Pick something'),
        password(name: 'PASSWORD', defaultValue: 'SECRET', description: 'Enter a password')
    ]),
    disableConcurrentBuilds(),
    buildDiscarder(logRotator(removeLastBuild: true, numToKeepStr: '5'))
])

// =============================================================================
// Helpers
// =============================================================================

// Emulates `options { skipStagesAfterUnstable() }`: every stage checks the build result first.
def runStage(String name, Closure body) {
    stage(name) {
        if (currentBuild.currentResult == 'UNSTABLE') {
            skipStage(name, 'build is UNSTABLE (skipStagesAfterUnstable)')
            return
        }
        body()
    }
}

// Emulates a stage skipped by `when {}` or by skipStagesAfterUnstable.
def skipStage(String name, String reason) {
    echo "Stage '${name}' skipped: ${reason}"
    // Optional: render the stage as "skipped" (grey) in Stage View / Blue Ocean, like declarative does.
    // Inside the Groovy sandbox this call needs a one-time In-process Script Approval by an admin:
    // org.jenkinsci.plugins.pipeline.modeldefinition.Utils.markStageSkippedForConditional(name)
}

// =============================================================================
// Pipeline: `agent any` => node {}
// =============================================================================
node {
    try {
        // options { timeout(time: 5, unit: 'MINUTES') }
        // Wraps the stages only, so the post actions in `finally` still run after a timeout.
        timeout(time: 5, unit: 'MINUTES') {

            // Declarative performs this implicitly ("Declarative: Checkout SCM"); scripted does not.
            stage('Checkout SCM') {
                checkout scm
            }

            runStage('Use shared library') {
                helloWorld(name: 'Moshe', userName: 'user mosheilan')
            }

            runStage('Checkout & Cleanup') {
                // when { branch pattern: "notMain", comparator: "EQUALS" }
                // BRANCH_NAME exists only in Multibranch jobs; elsewhere it is null => stage is skipped.
                if (env.BRANCH_NAME != 'notMain') {
                    skipStage('Checkout & Cleanup', "branch '${env.BRANCH_NAME}' does not equal 'notMain'")
                    return
                }
                // stash name: 'source', includes: '**'
                sh 'ls -shall'
                sh 'docker rm -f smoke-test || true'
            }

            runStage('Example') {
                echo "Toggle: ${params.TOGGLE}"
                echo "Choice: ${params.CHOICE}"
                // Single quotes: printed literally, never interpolated (same as the original, and keeps the secret out of the log).
                echo 'Password: ${params.PASSWORD}'
            }

            runStage('Run Tests') {
                // parallel {} => parallel(map). failFast defaults to false in both syntaxes.
                parallel(
                    'lint': {
                        runStage('lint') {
                            // Stage-level `agent { docker { image ... } }` => a NEW node (own workspace)
                            // + implicit checkout + container.
                            node {
                                checkout scm
                                docker.image('python:3.12-slim').inside {
                                    sh '''
                                        python -m venv .venv
                                        . .venv/bin/activate
                                        pip install ruff djlint
                                        ruff check app.py
                                    '''
                                }
                            }
                        }
                    },
                    'Test': {
                        runStage('Test') {
                            node {
                                checkout scm
                                try {
                                    docker.image('python:3.12-slim').inside {
                                        // FIX: the original only activated `.venv`, which lives in the lint
                                        // branch's separate workspace/container, so this stage always failed.
                                        sh '''
                                            python -m venv .venv
                                            . .venv/bin/activate
                                            pip install flask pytest
                                            pytest -v --junitxml=reports/pytest-report.xml
                                        '''
                                    }
                                } finally {
                                    // FIX: stash even when tests fail, so junit can publish the failures.
                                    stash includes: 'reports/*.xml', name: 'test-results', allowEmpty: true
                                }
                            }
                        }
                    }
                )
            }
            // Example of CPS bug
            def matcher = "app-v1.2.3" =~ /v(\d+\.\d+\.\d+)/
            sh 'echo "some step runs here"'
            echo "version is ${matcher[0][1]}"

            runStage('Build') {
                sh 'docker build -t my-flask-app:${BUILD_NUMBER} .'
            }

            runStage('Push') {
                // environment { DOCKER_REGISTRY = credentials('...') } for a Username/Password
                // credential => DOCKER_REGISTRY_USR / DOCKER_REGISTRY_PSW. Scoped to this stage only.
                withCredentials([usernamePassword(
                    credentialsId: '36304674-ec83-40bf-a83e-7fa73b31f653',
                    usernameVariable: 'DOCKER_REGISTRY_USR',
                    passwordVariable: 'DOCKER_REGISTRY_PSW'
                )]) {
                    // Single quotes: the SHELL expands the secret, Groovy never sees it (no leak, no warning).
                    sh '''
                        docker tag my-flask-app:${BUILD_NUMBER} local-registry:5000/my-flask-app:${BUILD_NUMBER}
                        echo "$DOCKER_REGISTRY_PSW" | docker login local-registry:5000 --username "$DOCKER_REGISTRY_USR" --password-stdin
                        docker push local-registry:5000/my-flask-app:${BUILD_NUMBER}
                    '''
                }
            }

            runStage('Smoke test') {
                // script {} is not needed: a scripted pipeline is already Groovy.
                sh '''
                    docker run -d --name smoke-test -p 5001:5001 \
                      local-registry:5000/my-flask-app:${BUILD_NUMBER}
                    sleep 3
                '''
                // FIX: `|| true` => on connection refused curl still prints "000" instead of aborting the
                // step, so the container logs are shown and the error message below is meaningful.
                def status = sh(
                    script: 'curl -s -o /dev/null -w "%{http_code}" http://docker:5001/ || true',
                    returnStdout: true
                ).trim()
                sh 'docker logs smoke-test'
                sh 'docker rm -f smoke-test'
                if (status != '200') {
                    error "Smoke test failed: expected 200, got ${status}"
                }
            }
        }
    } catch (org.jenkinsci.plugins.workflow.steps.FlowInterruptedException e) {
        // Timeout expiry or manual abort => ABORTED; declarative does NOT run `post { failure }` here.
        currentBuild.result = 'ABORTED'
        throw e
    } catch (e) {
        currentBuild.result = 'FAILURE'
        throw e
    } finally {
        stage('Post Actions') {
            // ---- post { always { ... } }  (declarative evaluates `always` BEFORE `failure`) ----
            // FIX: `|| true`; otherwise a missing container can fail the step and skip everything below.
            sh 'docker rm -f smoke-test || true'
            // FIX: if the Test stage never ran, unstash throws and would skip junit + cleanWs.
            try {
                unstash 'test-results'
            } catch (ignored) {
                echo 'No test results were stashed; skipping unstash.'
            }
            junit testResults: 'reports/pytest-report.xml', allowEmptyResults: true
            // Deletes only `.git` and keeps `reports/*`, so the failure block can still archive them.
            cleanWs(cleanWhenNotBuilt: false,
                    deleteDirs: true,
                    disableDeferredWipeout: true,
                    notFailBuild: true,
                    patterns: [[pattern: '.git', type: 'INCLUDE'],
                               [pattern: 'reports/*', type: 'EXCLUDE']])

            // ---- post { failure { ... } } ----
            if (currentBuild.currentResult == 'FAILURE') {
                echo 'Build failed! Archiving diagnostic logs and artifacts...'
                archiveArtifacts artifacts: 'reports/*.xml',
                                 allowEmptyArchive: true,
                                 fingerprint: true,
                                 onlyIfSuccessful: false
            }
        }
    }
}
