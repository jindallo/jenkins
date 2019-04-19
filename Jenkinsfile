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
        stage("Prepare") {
            steps{
                sh "/home/jenkins/replay.sh"
                sh "sleep 10"
            }
        }

        stage('Test') {
            steps {
                sh """
                    cd /home/jenkins/jenkins/workspace/ADAS_China/workdir/asimov
                    rm -rf venv
                    virtualenv --no-download venv -p python3.6
                    . venv/bin/activate
                    ./validation/init.sh
           	        cd ${test_dir_path}
                    rm -rf results
                    mkdir -p results
                    python -m pytest -vs test_uds_did_f101.py \
                        -- html=results/report.html \
                        -- log_dir_path results
                    deactivate
                """
            }
        }
    }
}
