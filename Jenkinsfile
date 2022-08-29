pipeline {
    agent any
    stages {

        stage("build") {
            steps{
                echo 'build'
                sh 'whoami'
                sh 'ls -lart'
                sh 'uname -a'
            }
        }

        stage("test") {
            steps{
                echo 'test'
            }
        }

        stage("deploy") {
            steps{
                echo 'deploy'
            }
        }
    }
}
