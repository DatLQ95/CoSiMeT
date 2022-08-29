pipeline {
    agent any
    stages {

        state("build") {
            steps{
                echo "build"
                sh "whoami"
                sh "ls -lart"
            }
        }

        state("test") {
            steps{
                echo "build"
            }
        }

        state("deploy") {
            steps{
                echo "build"
            }
        }
    }
}