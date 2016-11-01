node {
    def mvnHome = tool 'M3'

    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        sh "make dist"
    }

    stage('Archive') {
        archiveArtifacts artifacts: '**/*.zip', fingerprint: true
    }
}
