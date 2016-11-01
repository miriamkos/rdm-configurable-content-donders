node {
    def mvnHome = tool 'M3'

    stage('Checkout') {
        checkout scm
    }

    stage('Build') {
        sh "make dist"
        sh "${mvnHome}/bin/mvn -U clean package"
    }

    stage('Install') {
        sh "${mvnHome}/bin/mvn install"
    }

    stage('Analyse') {
        sh "${mvnHome}/bin/mvn sonar:sonar"
    }

    stage('Archive') {
        archiveArtifacts artifacts: '**/*.zip, **/target/*.zip', fingerprint: true
    }
}
