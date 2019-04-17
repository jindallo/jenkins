#!groovy

def Target = "${params.TargetNode}"
def WORKSPACE = "/home/jenkins/jenkins/workspace/ADAS_China/workdir/asimov"

pipeline {
    agent {
        customWorkspace "/home/jenkins/jenkins/workspace/ADAS_China/workdir/asimov/"
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
                    rm -rf venv
                    virtualenv venv -p python3.6
                    . venv/bin/activate
                    ./validation/init.sh
                    cd ${test_dir_path}
                    rm -rf results
                    mkdir -p results
                    date
                    python -m pytest -vs test_wakeup_time.py \
                                     --junitxml=results/result.xml \
                                     --log_dir_path results
                    date
                    deactivate
                """
            }
        }
    }
}
