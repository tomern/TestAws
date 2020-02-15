pipeline {
   agent any
   options{
        timestamps()
   }
   environment { 
	   PVWA_ADDRESS = ""
	   PVWA_INSTANCE_ID = ""
	   TEST_ADDRESS = ""
	   TEST_INSTANCE_ID = ""
   }
   stages {
      stage('NuGet Restore') {
         steps {  
            bat 'C:\\Users\\tomern23\\Downloads\\nuget.exe restore TestAws.sln'
         }
      }
      stage('Compiling') {
         steps {
            bat '"C:\\Program Files (x86)\\MSBuild\\14.0\\Bin\\MSBuild.exe" TestAws.sln'
         }
      }
      stage('Compress Code') {
         steps {
            script{
               zip zipFile: 'tests.zip', archive: false, dir: ''
               archiveArtifacts artifacts: 'tests.zip', fingerprint: true
            }
         }
      }
	  stage('Setup AWS Instances') {
		steps {	
                parallel(
                    'Start SUT Machine': {
                        bat 'C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/start_sut_machine.py'
						script{	
							PVWA_ADDRESS = readFile 'pvwa_ip.txt'
							PVWA_INSTANCE_ID = readFile 'pvwa_id.txt'
							echo PVWA_ADDRESS
							echo PVWA_INSTANCE_ID
						}
                    },
                    'Create Test Machine': {
                        bat "C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/create_machine.py"
						script{
							TEST_ADDRESS = readFile 'test_machine_ip.txt'
							TEST_INSTANCE_ID = readFile 'test_machine_id.txt'
							echo TEST_ADDRESS
							echo TEST_INSTANCE_ID
						}
					}
				)
			}
      } 
      stage('Copy Tests to Test Machine') {
	   steps {
		bat "C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/transfer.py ${TEST_ADDRESS} 1"
	   }
      }
      stage('Testing') {
	   steps {
		bat "C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/execute.py ${TEST_ADDRESS} ${PVWA_ADDRESS}"
	   }
      } 
      stage('Get Results') {
	   steps {
		bat "C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/transfer.py ${TEST_ADDRESS} 0"
	   }
      } 		
	  stage('Clean AWS Instances') {
	   steps {
		parallel(
		   'Terminate Test Machine': {
                        bat "C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/terminate_instance.py ${TEST_INSTANCE_ID}"
                    },
                   'Stop SUT Machine': {
                        bat "C:/Users/tomern23/AppData/Local/Programs/Python/Python37/python C:/Users/tomern23/PycharmProjects/manager/stop_instance.py ${PVWA_INSTANCE_ID}"
                }
		)
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

