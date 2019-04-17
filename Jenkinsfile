#!groovy

def Target_Node = "${params.TargetNode}"
def WORKSPACE = "/home/jenkins/jenkins/workspace/ADAS_China/workdir/asimov"

pipeline {
    agent {
        node {
            label "cn-rpi-tb-03"
            customWorkspace "/home/jenkins/jenkins/workspace/ADAS_China/workdir/asimov/"
        }
    }

    environment {
        test_dir_path = "validation/tests/boot/"
    }

    stages {
        stage('Test') {
            steps {
                sh """
           	        date
                    pwd
                    cd validation/tests/uds/
                    test_uds_did_f101.sh
                """
            }
        }
    }
}
