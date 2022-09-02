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
                echo 'Deploy'
                sh 'source /home/dat/CoSiMeT/venv/bin/activate'
                sh 'pyinstaller src/main.py -y'
            }
        }
    }
}
