def PVWA_ADDRESS
def TEST_ADDRESS

pipeline {
   agent any
   options{
        timestamps()
   }
   stages {
      stage('Restore Nuget') {
         steps {
            bat 'C:\\Users\\tomern23\\Downloads\\nuget.exe restore TestAws.sln'
         }
      }
      stage('Build') {
         steps {
            bat '"C:\\Program Files (x86)\\MSBuild\\14.0\\Bin\\MSBuild.exe" TestAws.sln'
         }
      }
      stage('Zip') {
         steps {
            script{
               zip zipFile: 'tests.zip', archive: false, dir: ''
               archiveArtifacts artifacts: 'tests.zip', fingerprint: true
            }
         }
      }
      stage('Create Test Machine') {
         steps {
            echo "current build number: ${currentBuild.number}"
            bat 'C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/entire_script.py'
            script{
                PVWA_ADDRESS = readFile 'pvwa.txt'
                echo PVWA_ADDRESS
                TEST_ADDRESS = readFile 'test_machine.txt'
                echo TEST_ADDRESS
             }
         }
      }
   }
    post {
      always {
         nunit testResultsPattern: 'TestResult.xml'
         deleteDir();
      }
    }
}
