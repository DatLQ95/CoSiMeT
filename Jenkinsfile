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
                echo 'build'
                sh 'whoami'
                sh 'ls -lart'
                sh 'uname -a'
            }
        }

        stage("deploy") {
            agent any
            steps{
                echo 'build'
                sh 'whoami'
                sh 'ls -lart'
                sh 'uname -a'
            }
        }
    }
}
