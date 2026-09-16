pipeline {
    agent any
    options {
        skipStagesAfterUnstable()
    }
stages {
  stage('wow') {
    steps {
      sh docker ps
    }
    input {
      message 'hi'
    }
  }

}
}
