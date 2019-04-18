#!groovy

def Target_Node = "${params.TargetNode}"

pipeline {
    agent {
        node {
            label "cn-rpi-tb-01"
            customWorkspace "/home/jenkins/jenkins/workspace/ADAS_China/workdir/test/"
        }
    }

    environment {
        test_dir_path = "validation/tests/uds"
        result_dir_path = "${test_dir_path}/results"
        owner_mail = "zhouting.xie.o@nio.com"
    }

    stages {
        stage('Test') {
            steps {
                sh """
           	        date
                    pwd
                """
            }
        }
    }
}
