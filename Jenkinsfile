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
		            echo "pkill canplayer -f" > ~/pkcan.sh
                    echo "pkill cangen -f" >> ~/pkcan.sh
                    echo "return 0" >> ~/pkcan.sh
                    chmod 777 ~/pkcan.sh
                    ~/pkcan.sh
                    cd validation/tests/uds/
                    ./test_uds_f101_full_function.sh --log_dir_path "/home/jenkins/jenkins/workspace/ADAS_China/workdir/log"
                """
            }
        }
    }
}
