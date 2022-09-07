pipeline {
    agent none
    stages {

        stage("build") {
            agent { label 'nl-cs' }
            steps{
                echo 'build'
                sh 'whoami'
                sh 'ls -lart'
                sh 'uname -a'
            }
        }

        stage("test") {
            agent { label 'jenkins' }
            steps{
                echo 'Test'
                sh 'whoami'
                sh 'ls -lart'
                sh 'uname -a'
            }
        }

        stage("deploy") {
            agent { label 'nl-cs-glicci' }
            steps{
                sh 'whoami'
                echo 'Deploy'
                sh "export COSIMET_DB_TABLE=servers"
                sh """. /home/dat/CoSiMeT/venv/bin/activate
                pip install -r requirements.txt
                pyinstaller src/main.py -y"""
            }
        }
    }
}
