node {
    def mvnHome = tool 'M3'
    try {
        stage('Checkout') {
            checkout scm
        }

        stage('Build') {
            sh 'echo "Git hash: `git rev-parse --verify HEAD` , Build on `date`" > build.txt'
            sh "make dist"
        }

        stage('Archive') {
			archiveArtifacts artifacts: '**/rdm-configurable-content-*', fingerprint: true
        }
    } finally {
        deleteDir()
    }
}