pipeline {
    agent any
    stages {

        state("build") {
            steps{
                echo 'build'
                sh 'whoami'
                sh 'ls -lart'
            }
        }

        state("test") {
            steps{
                echo 'test'
            }
        }

        state("deploy") {
            steps{
                echo 'deploy'
            }
        }
    }
}
