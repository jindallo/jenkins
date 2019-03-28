#!groovy

node('master') {

    stage('Build') {
        echo 'Hello World 1'
        sh 'echo $params.TargetNode'
        echo 'echo $params.TargetNode'
    }
    
    stage('Test') {
        echo 'Hello World 2'
    }

    stage('Deploy') {
        echo 'Hello World 3'
    }
}
