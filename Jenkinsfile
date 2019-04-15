#!groovy

def Target = "${params.TargetNode}"
def WORKSPACE = "/home/jenkins/jenkins/workspace/ADAS_China/workdir/asimov"

node('master') {

    stage('Build') {
        echo 'Hello World 1'
        sh 'cd $WORKSPACE'
        sh 'pwd'
    }
    
    stage('Test') {
        echo 'Hello World 2'
    }

    stage('Deploy') {
        echo 'Hello World 3'
    }
}
