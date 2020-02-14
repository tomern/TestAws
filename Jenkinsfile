def PVWA_ADDRESS
def TEST_ADDRESS

pipeline {
   agent any
   options{
        timestamps()
   }
   stages {
      stage('Create Test Machine') {
         steps {
            echo "current build number: ${currentBuild.number}"
            bat 'C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/create_test_machine_mono.py'
         }
      }
      stage('Get PVWA address') {
         steps {
             script{
                PVWA_ADDRESS = readFile 'pvwa.txt'
                echo PVWA_ADDRESS
             }
         }
      }
      stage('Get Test Machine address') {
         steps {
             script{
                TEST_ADDRESS = readFile 'test_machine.txt'
                echo TEST_ADDRESS
             }
         }
      }
      stage('Copy Artifactory to Test Machine') {
         steps {
            bat 'python C:/Users/tomern23/PycharmProjects/manager/copyartifacoty.py'
         }
      }
      stage('Run Tests') {
         steps {
            bat 'C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/script.py'
         }
      }
   }
    post {
        always {
            deleteDir();
            //nunit testResultsPattern: '*TestResult*.xml'
        }
    }
}