node {
    stage('Build') {
        echo 'Build'
    }
    stage('Test') {
        echo 'Test'
    }
    if (currentBuild.currentResult != 'SUCCESS') {
    stage('Deploy') {
        echo 'Deploy'
    }
    }
}
